from google.cloud import bigquery
from google.api_core import exceptions as gcx

field_list = ['product',
              'product_version',
              'timestamp',
              'testsuite',
              'testcase',
              'status',
              'assertion',
              'input',
              'execution_duration',
              'raw_failure_txt'
              ]


def get_bq_schema(field_list):
    schema: list = list()
    for field in field_list:
        if field == 'internal_timestamp':
            schema.append(bigquery.SchemaField(name=field, field_type='TIMESTAMP'))
        else:
            schema.append(bigquery.SchemaField(name=field, field_type='STRING'))
    return schema

# TODO MERGE HELPERS AND BQ_SCHEMA