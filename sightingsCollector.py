from lxml import html

import requests
import json
import re

class Sighting():
    def __init__(self, data):
        self.data = data
        self.date = data[0].split(', ')[0]
        self.time = data[0].split(', ')[1]
        self.duration = data[1]
        self.maxHeight = data[2]
        self.appear = data[3].replace('  ', ' ')
        self.disappear = data[4].replace('  ', ' ')

def getSightings(country, region, city):
    url = 'https://spotthestation.nasa.gov/sightings/view.cfm?'
    url += 'country=%s&region=%s&city=%s' % (country, region, city)

    page = requests.get(url)
    tree = html.fromstring(page.content)

    summaryTemplate = 'Sighting table for %s, %s, %s'
    summary = summaryTemplate % (city, region, country)
    contents = tree.xpath('//table[@summary="%s"]/tr/td/text()' % summary)

    numberOfRows = len(contents) // 9
    sightings = []
    for row in range(numberOfRows):
        data = contents[9*row:9*row + 5]
        sightings.append(Sighting(data))

    return sightings

siteDataJson = ''.join(open('siteData.json', 'r').readlines())
siteData = json.loads(siteDataJson)

stopWordsData = open('stopWords.txt', 'r').readlines()
stopWords = [line.strip().lower() for line in stopWordsData]

countries = {}
regions = {}
cities = {}

for c in siteData.keys():
    regionData = [r for r in siteData[c]['Regions'] if r['RegionName'] != 'None']
    regions = dict([[r['RegionName'], r['RegionCode']] for r in regionData])

    for rIndex in range(len(regions.keys())):
        cityData = siteData[c]['Regions'][rIndex]['Cities']

        for city in cityData:
            key = city['CityCode']
            regionCode = regions[list(regions.keys())[rIndex]][len(c)+1:]
            
            value = [c, regionCode, city['CityName'].replace(' ', '_')]
            cities[key] = value

while True:
    print("Enter something someone might tweet.")
    response = input().lower()
    words = re.findall(r"[\w']+", response)

    if response == 'exit':
        break

    matchingKeys = []
    desiredCity = ''
    
    for word in [w for w in words if w not in stopWords]:
        matchingKeys += [key for key in cities.keys() if word in key.lower()]
        
    if (len(matchingKeys) > 1):
        print("Your query matched %d cities:" % len(matchingKeys))

        for key in matchingKeys:
            data = cities[key]
            print("%s, %s" % (data[2], data[1]))

        region = input("Which region is it? ")
        desiredCity = [key for key in matchingKeys if region in cities[key][1]][0]

    elif (len(matchingKeys) == 1):
        desiredCity = matchingKeys[0]

    else:
        print("I don't know any cities by that name.")
        continue

    params = cities[desiredCity]
    sightings = getSightings(params[0], params[1], params[2])

    if len(sightings) > 0:
        message = "The next time you'll be able to see the International Space " + \
            "Station will be on %s at %s. It'll be overhead for about %s moving " + \
            "from %s to %s."

        s = sightings[0]
        print (message % (s.date, s.time, s.duration, s.appear, s.disappear))
        break

    else:
        print("You will not be able to see the International Space Station " + \
              "for quite a while. Ask me again in a week or so.")
