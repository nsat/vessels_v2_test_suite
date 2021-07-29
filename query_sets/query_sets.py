from gql import gql
from loguru import logger


class GetQuery(object):

    def __init__(self):
        self._query_text = """
           query {
                  vessels(
                    first: 1000
                  ) {
                    pageInfo{
                      hasNextPage
                      correlationId
                      endCursor
                    }
                    nodes {
                      ingestionTimestamp
                      staticInfo {
                        flag
                        name
                        class
                        callsign
                        timestamp
                        ingestionTimestamp
                        imo
                        mmsi
                        shipType
                        dimensions {
                          width
                          length
                        }
                         antennaDistances {
                              a
                              b
                              c
                              d
                            }
                      }
                      lastPositionUpdate {
                        accuracy
                        heading
                        latitude
                        longitude
                        collectionType
                        maneuver
                        timestamp
                        ingestionTimestamp
                        navigationalStatus
                        rot
                        speed
                      }
                      currentVoyage {
                        reportedETA
                        draught
                        reportedDestination
                        ingestionTimestamp
                        timestamp
                      }
                    }
                  }
                }      
        """

    def get_query_from_file(self, file):
        """
        Parameters: file(str) full path to query file
        Returns: query(str)
        """
        query: str = str()
        try:
            with open(file, 'r') as f:
                query = f.read()
        except FileNotFoundError as e:
            logger.error(f"Can not find query text file: {file} ")
            raise
        return query



    def get_vessel_query_text(self):
        return self._query_text


    def get_vessels_gql_query(self):
        return gql(self.get_vessel_query_text())


    def get_matched_port_gql_query(self, input_text=''):
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
        return gql(q)


    def get_port_gql_query(self, input_text=''):
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
        return gql(q)

