from lxml import html
import requests

class Sighting():
    def __init__(self, data):
        self.data = data
        self.date = data[0]
        self.duration = data[1]
        self.maxHeight = data[2]
        self.appear = data[3]
        self.disappear = data[4]

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

sightings = getSightings('Afghanistan', 'None', 'Kabul')

for s in sightings:
    print('\t'.join(s.data))
