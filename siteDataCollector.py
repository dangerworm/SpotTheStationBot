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

output = open('siteData.json', 'w')
output.write('{\n')
output.flush()

lastCountry = list(countries.keys())[-1]
for country in countries.keys():
    print('Getting data for %s' % country)

    countries[country] = {}

    connection.request('GET', '/sightings/location_files/%s.cfm' % country)
    response = connection.getresponse()
    regions = getDict(response)

    output.write('\t"%s":\n' % country)
    output.write('\t{\n')
    output.write('\t\t"CountryCode": "%s",\n' % country)
    output.write('\t\t"CountryName": "%s",\n' % country.replace('_', ' '))
    output.write('\t\t"Regions":\n')
    output.write('\t\t[\n')
    output.flush()

    lastRegion = list(regions.keys())[-1]
    for region in regions.keys():
        ## countries[country][region] = {}
        
        connection.request('GET', '/sightings/location_files/%s.cfm' % region)
        response = connection.getresponse()
        cities = getDict(response)

        countries[country][region] = cities

        output.write('\t\t\t{\n')
        output.write('\t\t\t\t"RegionCode": "%s",\n' % region)
        output.write('\t\t\t\t"RegionName": "%s",\n' % regions[region])
        output.write('\t\t\t\t"Cities":\n')
        output.write('\t\t\t\t[\n')
        output.flush()

        lastCity = list(cities.keys())[-1]
        for city in cities.keys():
            output.write('\t\t\t\t\t{\n')
            output.write('\t\t\t\t\t\t"CityCode": "%s",\n' % city)
            output.write('\t\t\t\t\t\t"CityName": "%s"\n' % cities[city])

            comma = '' if city == lastCity else ','
            output.write('\t\t\t\t\t}%s\n' % comma)
            output.flush()

        output.write('\t\t\t\t]\n')
        output.flush()

        comma = '' if region == lastRegion else ',' 
        output.write('\t\t\t}%s\n' % comma)
        output.flush()

    output.write('\t\t]\n')
    comma = '' if country == lastCountry else ','
    output.write('\t}%s\n' % comma)
    output.flush()
        
output.write('}\n')
output.close()
