import http.client

def getSightings(country, region, city):
    connection = http.client.HTTPSConnection('spotthestation.nasa.gov')
    url = '/sightings/view.cfm?'
    params = 'country=%s&region=%s&city=%s' % (country, region, city)

    connection.request('GET', url + params)
    return connection.getresponse().readlines()

print(getSightings('Afghanistan', 'None', 'Kabul')[0:5])
