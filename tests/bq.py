from google.cloud import bigquery
from google.api_core import exceptions as gcx
from conftest import get_settings
import xmltodict
from nested_lookup import nested_lookup as nl
import os
from helpers import v2_schema, test_results_field_list
from loguru import logger
from datetime import datetime
from time import sleep

class BQ(object):

    def __init__(self,
                 gcp_project_id,
                 gcp_dataset_id,
                 gcp_table_id,
                 field_list,
                 partition=True):
        self._partition = partition
        settings = get_settings()
        self._client = bigquery.Client(project=gcp_project_id)
        bigquery.DEFAULT_RETRY.with_deadline(10)
        self._dataset_reference = bigquery.dataset.DatasetReference(project=gcp_project_id,
                                                                    dataset_id=gcp_dataset_id)
        self._table_reference = bigquery.table.TableReference(dataset_ref=self._dataset_reference,
                                                              table_id=gcp_table_id)
        self._pytest_xml_report_path = settings['pytest_xml_report_path']
        self._schema = self._build_schema(field_list)
        self._field_list = field_list
        self._create_dataset()
        self._create_table()

    def _create_dataset(self):
        dataset = bigquery.Dataset(self._dataset_reference)
        try:
            self._client.create_dataset(dataset)
        except (gcx.AlreadyExists, gcx.Conflict):
            logger.debug("Dataset already exists, this may be an expected condition")
            return
        logger.debug(f'Dataset created')
        try:
            self._client.get_dataset(dataset_ref=self._dataset_reference)
        except gcx.NotFound as e:
            msg = f"""
            Can not verify existing dataset
            {e}
            """
            logger.error(msg)
            raise gcx.NotFound(msg)
        logger.debug("Dataset confirmed")

    def _create_table(self):

        """Creates a table for test results if one does not exist
        """

        table = bigquery.Table(self._table_reference, self._schema)
        if self._partition:
            table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY,
                                                                field='row_insert_timestamp',
                                                                expiration_ms=7776000000)
        try:
            self._client.create_table(table)
        except (gcx.AlreadyExists, gcx.Conflict):
            logger.info("Table already exists, this may be an expected condition")
            return
        logger.debug(f'Table created')
        try:
            self._client.get_table(table)
        except gcx.NotFound:
            logger.error(f'ERROR: Can not verify existing table')
            raise Exception
        except (ValueError, gcx.BadRequest) as e:
            logger.error(e)
            raise
        logger.debug("Table confirmed")

    def insert_rows(self, rows):
        """Insert rows into the bq table 
        """
        table = self._client.get_table(self._table_reference)
        logger.debug("ATTEMPTING TO WRITE BQ ROWS TO TABLE")

        try:
            for row in rows:
                errors = self._client.insert_rows(self._table_reference, [row], selected_fields=table.schema)
                if errors:
                    logger.error(f"""BQ ERROR: 
                    {errors}""")

            logger.info(f"{len(rows)} BQ ROWS INSERTED")
        except gcx.BadRequest as b:
            logger.error(b)
            raise

        except OverflowError as e:
            logger.error(f"""
            Ignoring this OverflowError, just skipping this row
            {e}""")
        except ValueError as e:
            logger.error(e)

    def parse_test_results(self):
        """Parses pytest test results xml file
        The output dictionary has the following structure:
        ['testsuites'] - OrderedDict
            ['testsuite'] - OrderedDict
                ... ['@timestamp']
                    ['testcase'] - OrderedDict
                        ['00'] - OrderedDict
                            ['@classname'] - parsed to test suite name
                            ['@name'] - parsed to test name and input value
                            ['@time'] - execution duration
                            ['failure'] - OrderedDict (optional, not all entries have one
                                ['@message'] - the assertion message
                                ['#text'] - the raw failure output text from pytest.. it's LONG
        """
        # todo try, except FileNotFound
        with open(self._pytest_xml_report_path) as ifp:
            # dict.setdefault(key, default=None)
            results_dictionary: dict = xmltodict.parse(ifp.read())
        return results_dictionary

    def _parse_name(self, string):
        """Cleans up the test name 'test_NAME[input_value]' and splits it into a name and input value
        :param string: string to parse
        :type string: str
        :returns testname, inputvalue: cleanded up name of the test and the test input value
        :rtype testname, inputvalue: str, str
        """
        if '[' and ']' not in string:
            return string.replace('test_', ''), ''
        loc1: int = string.find('[')
        loc2: int = string.find(']')
        inputvalue: str = string[loc1 + 1: loc2]

        if not inputvalue:
            temp: str = string.replace(f'[{inputvalue}]', '')
            inputvalue = 'NA'
        else:
            temp: str = string.replace(f'[{inputvalue}]', '')
        testname: str = temp.replace('test_', '')
        return testname, inputvalue

    def build_test_case_dict(self, data):
        """Creates dictionary of test data
        :param data: from pytest results processing
        :type data: dict

        """
        settings = get_settings()
        rows: list = list()
        info: dict = dict()
        key: str
        for key in self._field_list:
            info.setdefault(key, '')
        # get test suite name
        testcases = nl('testcase', data)
        try:
            test = testcases[0]
        except IndexError as e:
            logger.error(f"""
            data: {data}
            error: {e}
            """)

        info['testsuite'] = test['@classname'].replace('tests.test_', '')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info['timestamp'] = timestamp
        info['product_version'] = settings['product_version_under_test']
        info['product'] = settings['product_under_test']
        test_name, input_value = self._parse_name(test['@name'])
        info['testcase'] = test_name
        info['input'] = input_value
        info['execution_duration'] = test['@time']
        if len(test) == 3:
            info['status'] = "PASS"
        else:
            info['status'] = "FAIL"
            info['assertion'] = test['failure']['@message'].replace('AssertionError: ', '')
            info['raw_failure_txt'] = test['failure']['#text']
        rows.append(info)
        return rows



    def _build_schema(self, info):
        result: list = list()
        for field in info:
            if field == 'row_insert_timestamp':
                result.append(bigquery.SchemaField(name=field, field_type='TIMESTAMP'))
            else:
                result.append(bigquery.SchemaField(name=field, field_type='STRING'))
        return result


def write_captured_data(data: dict, test_name: str = '', test_execute_start_time: str = ''):
    """:returns
    bigquery.DEFAULT_RETRY.with_deadline(30)
    """
    settings = get_settings()
    bq = BQ(gcp_project_id=settings['gcp_project_id'],
            gcp_dataset_id=settings['captured_data_dataset_id'],
            gcp_table_id=settings['captured_data_table_id'],
            field_list=v2_schema)
    vessels: list = nl('vessel', data)
    positionUpdate: list = nl('positionUpdate', data)
    voyages: list = nl('voyage', data)

    # flatten the dictionaries and add to rows list
    flats: list = list()
    for idx in range(len(vessels)):
        flat: dict = dict()
        flat['row_insert_timestamp'] = "AUTO"
        flat['test_execute_start_time'] = test_execute_start_time
        flat['test_name'] = test_name
        for key in v2_schema:
            flat.setdefault(key, '')

        # add vessel data to the flat dictionary
        vessel: dict = vessels[idx]
        position: dict = dict()
        if vessel:
            for k, v in vessel.items():
                if k == 'dimensions':
                    dimensions = vessel['dimensions']
                    for item, value in dimensions.items():
                        if value:
                            flat[item] = value
                if k == 'timestamp':
                    k = 'vessel_timestamp'
                if not v:
                    v = ''
                if not k == 'dimensions':
                    flat[k] = v
            # if there is position data, add to flat 

            try:
                position = positionUpdate[idx]
            except IndexError:
                # there is no position, so add the current flat to flat list
                flats.append(flat)
        if position:
            for k, v in position.items():
                if k == 'timestamp':
                    k = 'position_timestamp'
                if not v:
                    v = ''
                flat[k] = v
        voyage: dict = dict()
        try:
            voyage = voyages[idx]
        except KeyError:
            pass
        if not voyage:
            # there is no voyage, so add the current flat to flat list
            flats.append(flat)
        elif voyage:
            for k, v in voyage.items():
                if k == 'timestamp':
                    k = 'voyage_timestamp'
                if not v:
                    v = ''
                flat[k] = v
            flats.append(flat)
    bq.insert_rows(flats)


def write_test_results():

    logger.debug("ATTEMPTING TO WRITE TEST RESULTS")
    settings = get_settings()
    bq = BQ(gcp_project_id=settings['gcp_project_id'],
            gcp_dataset_id=settings['gcp_dataset_id'],
            gcp_table_id=settings['gcp_table_id'],
            field_list=test_results_field_list,
            partition=False)
    file = settings['pytest_xml_report_path']
    if not os.path.exists(file):
        sleep(3)
    elif os.path.exists(file):
        logger.debug(f"""READING TEST RESULTS FILE: {file}""")
        data: dict = bq.parse_test_results()
        rows = bq.build_test_case_dict(data)
        bq.insert_rows(rows)
        logger.debug("TEST RESULTS WRITTEN TO BQ")
        try:
            os.remove(file)
            logger.debug("TESTS RESULTS FILE REMOVED")
        except FileNotFoundError as e:
            logger.debug(e)

    else:
        logger.debug("NO TEST RESULTS FILE FOUND")