# SpotTheStationBot
This will be my first Twitter bot once I get it up and running. It's very quick and dirty,
but I just fancied having a go.

## siteDataCollector
First step was to scrape all the countries, regions and cities from the SpotTheStation web site. 
As this would only be run once I didn't spend long making it pretty, so all it does it make a
manual JSON file with the names and codes of the various sites organised hierarchically. 

## sightingsCollector
Once I had the site data I used them to form a basic data structure in memory. With some stop
words and a bit of logic I then attempted to figure out which city the user was interested in.

Finally, I did some more scraping of the STS site to get the latest times and positions.


