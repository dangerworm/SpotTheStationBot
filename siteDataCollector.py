import http.client

def getDict(responseString):
    strippedItems = [line.strip() for line in response.readlines()]
    decodedItems = [i.decode('ascii') for i in strippedItems]
    items = [i for i in decodedItems if len(i) > 0]

    output = {}
    for item in items:
        name = item.split('">')[1]
        code = item[15:len(item)-len(name)-2]
        output[code] = name

    return output

countriesInput = open('countries.txt', 'r')
countriesLines = [line.strip() for line in countriesInput.read().split('\n')]
countries = dict([line, {}] for line in countriesLines)

connection = http.client.HTTPSConnection('spotthestation.nasa.gov')

output = open('siteData.txt', 'w')

for country in countries.keys():
    print(country)
    output.write(country + '\n')
    output.flush()
    connection.request('GET', '/sightings/location_files/%s.cfm' % country)
    response = connection.getresponse()
    regions = getDict(response)

    countries[country] = {}

    for region in regions.keys():
        regionKey = region + ':' + regions[region]
        output.write('    ' + regionKey + '\n')
        connection.request('GET', '/sightings/location_files/%s.cfm' % region)
        response = connection.getresponse()
        cities = getDict(response)

        countries[country][regionKey] = cities

        for city in cities.keys():
            cityKey = city + ':' + cities[city]
            output.write('        ' + cityKey + '\n')

output.close()
