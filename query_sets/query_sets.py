from gql import gql


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
                      vessel {
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
                          a
                          b
                          c
                          d
                          width
                          length
                        }
                      }
                      positionUpdate {
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
                      voyage {
                        eta
                        draught
                        destination
                        ingestionTimestamp
                        timestamp
                      }
                    }
                  }
                }      
        """

    def get_query_from_file(self):
        pass


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
