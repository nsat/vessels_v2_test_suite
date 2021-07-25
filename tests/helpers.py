import requests
from gql import gql
from datetime import datetime, timedelta
import json, yaml
from loguru import logger
from nested_lookup import nested_lookup as nl
from string import Formatter


def get_settings():
    """Reads the settings.yaml file and returns the variables and values
    :returns data: setting variables and values
    :rtype data: dict
    """
    with open('settings.yaml') as f:
        data: dict = yaml.load(f, Loader=yaml.FullLoader)
    return data


def v1_request(params=''):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lciI6eyJpZCI6IjE2NjYiLCJuYW1lIjoidjFpbnRlcm5hbCIsInV1aWQiOiIxNjY2In0sImlzcyI6InNwaXJlLmNvbSIsImlhdCI6MTYyMjc2MTU5OX0.4TI0pnjnodyjyDjuW69JW7I1E4xkGP76vCLzRybSAzA'
    url = 'https://ais.spire.com/vessels?'
    headers = dict()
    headers['Authorization'] = f'Bearer {token}'
    headers['Content-type"'] = 'application/json'
    response = requests.get(url, headers=headers, params=params).json()
    return response


PositionCollectionType = [
    "DYNAMIC",
    "SATELLITE",
    "TERRESTRIAL"
]

test_results_field_list = ['product',
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

v2_schema = [
    'row_insert_timestamp',
    'test_execute_start_time',
    'test_name',
    'vessel_timestamp',
    'mmsi',
    'imo',
    'name',
    'callsign',
    'shipType',
    'class',
    'flag',
    'length',
    'width',
    'a',
    'b',
    'c',
    'd',
    'position_timestamp',
    'latitude',
    'longitude',
    'heading',
    'speed',
    'rot',
    'accuracy',
    'maneuver',
    'course',
    'navigationalStatus',
    'collectionType',
    'voyage_timestamp',
    'draught',
    'eta',
    'destination'
]

def get_matched_port_query(input_text=''):
    q: str = f"""
        query {{
            matchedPort{input_text}
            {{
                matchScore
                port {{
                    name
                    unlocode
                    centerPoint {{
                        latitude
                        longitude
                    }}
                
                }}
            }}
        
        }}
    """
    qn = q.replace("'", '"')
    logger.trace(f"""
           QUERY SUBMITTED:
           {qn}
           """"")
    return gql(qn)


def get_port_query(input_text=''):
    q: str = f"""
        query {{
            port{input_text}
            {{
                name
                unlocode
                centerPoint {{
                      latitude
                      longitude
                    }}
            }}
        }}
    """
    qn = q.replace("'", '"')
    logger.trace(f"""
        QUERY SUBMITTED:
        {qn}
        """"")
    return gql(qn)



def get_query(input_text=''):
    q: str = f"""
    query {{
            vessels{input_text}{{
                metadata{{
                    cursor
                    correlationId
                    after
                    hasMore
                }}
                vessels{{
                    vessel{{
                        name
                        flag
                        class
                        callsign
                        timestamp
                        mmsi
                        imo
                        shipType    
                        dimensions{{
                            a
                            b
                            c
                            d
                            length
                            width
                        }}
        
                    }}
                    voyage{{
                        eta
                        draught
                        timestamp
                        destination            
                    }}
                    positionUpdate{{
                        accuracy
                        timestamp
                        latitude
                        longitude
                        collectionType
                        heading
                        speed
                        rot
                        maneuver
                        course
                        navigationalStatus
                    }}
                }}
                
            }}        
    }}
    
    """
    qn = q.replace("'", '"')

    logger.trace(f"""
    QUERY SUBMITTED:
    {qn}
    """"")
    return gql(qn)


def get_route_query(input_text=''):
    q: str = f"""
     query {{ 
        vesselRoute{input_text}{{
             journey{{
                ...RouteDetails
            }}
            itinerary{{
                ...RouteDetails
            }}
            fragment PortDetails on Port {{
                  name
                  unlocode
                  centerPoint {{
                    latitude
                    longitude
                  }}
                }}
            fragment RouteDetails on Route {{
                  origin {{
                    ...PortDetails
                  }}
                  destination {{
                    ...PortDetails
                  }}
                  duration
                  distance
                  seca
                  eta
                }}
     
     }}"""

    qn = q.replace("'", '"')

    logger.trace(f"""
    QUERY SUBMITTED:
    {qn}
    """"")
    return gql(qn)


def write_orphans(data):
    log: str = get_settings()['in_v1_not_v2_log']
    d: dict = dict()
    keys = ['mmsi', 'imo', 'callsign', 'name']
    with open(log, 'a+') as f:
        for k, v in data.items():
            if k in keys:
                d[k] = v
        w = json.dumps(d, indent=4)
        f.write(w)


INDIAN_OCEAN = {
    "type": "Polygon",
    "coordinates": [
        [
            [
                51.31688050404585,
                -5.9765625

            ],
            [
                51.31688050404585,
                12.12890625

            ],
            [
                61.39671887310411,
                12.12890625

            ],
            [
                61.39671887310411,
                -5.9765625

            ],
            [
                51.31688050404585,
                -5.9765625
            ]
        ]
    ]
}

AOI = """{
            geoJson: {
                    type: 'Polygon'
                    coordinates: [
                        [
                            [   
                                51.31688050404585,
                                -5.9765625
                                
                            ],
                            [
                                51.31688050404585,
                                12.12890625
                                
                            ],
                            [   
                                61.39671887310411,
                                12.12890625
                                
                            ],
                            [
                                61.39671887310411,
                                -5.9765625
                                
                            ],
                            [
                                51.31688050404585,
                                -5.9765625
                                
                            ]
                        ]
                    ]
                }
        }
    """

WKT = '"POLYGON ((51.31688050404585 -5.9765625 , 51.31688050404585 12.12890625,  61.39671887310411 12.12890625,  61.39671887310411 -5.9765625,  51.31688050404585 -5.9765625))" '


def _is_within(given_time, start_time=None, end_time=None):
    now = datetime.utcnow()
    new_given_time = datetime.strptime(given_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    if start_time:
        # allow some time zone slop
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ") - timedelta(days=2)
    else:
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ") - timedelta(days=30)
    if end_time:
        # allow some time zone slop

        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(days=2)

    else:
        end_time = now
    return start_time < new_given_time <= end_time


def valid_timerange(data, start_time, end_time):
    vessels: list = nl('vessel', data)
    for vessel in vessels:
        timestamp = vessel['timestamp']
        if not _is_within(given_time=timestamp, start_time=start_time, end_time=end_time):
            v: dict = dict()
            for key, value in vessel.items():
                if value:
                    v[key] = value
            logger.error(f'FAILED TIMERANGE CHECK {v}')
            return False
        return True


def strfdelta(tdelta, fmt='{H:02}:{M:02}:{S:02.4f}', inputtype='timedelta'):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        '{D:02}d {H:02}h {M:02}m {S:02.0f}s' --> '05d 08h 04m 02s' (default)
        '{W}w {D}d {H}:{M:02}:{S:02.0f}'     --> '4w 5d 8:04:02'
        '{D:2}d {H:2}:{M:02}:{S:02.0f}'      --> ' 5d  8:04:02'
        '{H}h {S:.0f}s'                       --> '72h 800s'

    The inputtype argument allows tdelta to be a regular number instead of the
    default, which is a datetime.timedelta object.  Valid inputtype strings:
        's', 'seconds',
        'm', 'minutes',
        'h', 'hours',
        'd', 'days',
        'w', 'weeks'
    """

    # Convert tdelta to integer seconds.
    if inputtype == 'timedelta':
        remainder = tdelta.total_seconds()
    elif inputtype in ['s', 'seconds']:
        remainder = float(tdelta)
    elif inputtype in ['m', 'minutes']:
        remainder = float(tdelta)*60
    elif inputtype in ['h', 'hours']:
        remainder = float(tdelta)*3600
    elif inputtype in ['d', 'days']:
        remainder = float(tdelta)*86400
    elif inputtype in ['w', 'weeks']:
        remainder = float(tdelta)*604800

    f = Formatter()
    desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
    possible_fields = ('Y','m','W', 'D', 'H', 'M', 'S', 'mS', 'µS')
    constants = {'Y':86400*365.24,'m': 86400*30.44 ,'W': 604800, 'D': 86400, 'H': 3600, 'M': 60, 'S': 1, 'mS': 1/pow(10,3) , 'µS':1/pow(10,6)}
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            Quotient, remainder = divmod(remainder, constants[field])
            values[field] = int(Quotient) if field != 'S' else Quotient + remainder
    return f.format(fmt, **values)