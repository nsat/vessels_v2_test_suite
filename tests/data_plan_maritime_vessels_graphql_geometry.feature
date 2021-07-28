# Created by brucebookman at 7/25/21
Feature: # Enter feature name here
  # Enter feature description here

  
Scenario Outline: Limit results to specific AOI
    When the gql client is authenticated by an "<authorization_token>"
    Then the data returned will be limited to the "<aoi>"

    Examples:
    |authorization_token                |aoi  |
    |hYUxOeblNr3ga6b9z3fW9WeSylfQxMk5   |A    |
    |LlJja7jzt7hbYMDzk4rMU98GJeBXQJLN   |B    |
    |oIu2reNQxmXovmFOqD1OhUyBKaYqkqBs   |C    |


# AOI A: POLYGON ((-97 31, -80 31, -80 17, -97 17, -97 31))
# AOI B: POLYGON ((137.1014670789966 53.39764252638172, 137.911035263692 53.56381156398729,
#                 139.7815633187679 53.96832770935972, 140.8277007804127 53.26062815068768,
#                 141.123194837209 52.12024807464893, 139.8751191293523 48.41441834574981,
#                138.2470586745782 46.42687626697432, 141.720407302651 45.36687794362361,
#                143.4527526625995 44.11363684755314, 145.380302858699 44.01368470229303,
#                152.0333474915815 46.80921149148645, 156.0816609411319 50.48298862220748,
#                156.7862488949855 51.21447621453935, 155.609025529811 56.02681545777538,
#                157.5470131855306 57.36631895103271, 164.2581741275244 60.97780621342671,
#                165.6805879037394 62.83209912407987, 163.3697779906262 62.606199540633,
#                162.4323502387915 61.89941156528769, 160.7047150017666 60.83153496115801,
#                160.2705626922787 62.05752087278601, 157.0700404305677 61.82295534715772,
#                154.106293815187 59.91483654527536, 154.6983153369002 59.39144047876197,
#                152.8160672547206 59.1872469324572, 150.1396674499801 59.99959114662551,
#                149.0635369391001 59.32946212495977, 142.4658820184649 59.57564215857347, 134.9690518350559 55.02027310556164,
#                137.1014670789966 53.39764252638172))

# AOI C: POLYGON ((1.12884521484375 51.08195915715054, 1.60675048828125 50.6503312283444, 2.086029052734375 50.98264080879975, 1.39251708984375 51.19139393653174,
#                 1.12884521484375 51.08195915715054))

