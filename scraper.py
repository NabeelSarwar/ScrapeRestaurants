# -*- coding: utf-8 -*-
import urllib2 as urllib2
import re
import sys

# load urls
if len(sys.argv) == 2:
    f = open(sys.argv[1])
else:
    f = open('urls.txt')

listOfUrls = [line for line in f]

# make regexes
regexName = r'title>(\d*([A-Za-z’]+(\s|\s&amp;\s)?\b)+)'
regexName = re.compile(regexName)

regexStreet = r'ss>\s*(\d{1,5}( \w+){1,5})'
regexStreet = re.compile(regexStreet)

regexCity = r'ss>\s*\d{1,5}( \w+){1,5}, (([A-Za-z]+\s*)+),'
regexCity = re.compile(regexCity)

regexState = r',(\s[A-Z]{2}\s)'
regexState = re.compile(regexState)

regexZipcode = r'(\s[0-9]{5})'
regexZipcode = re.compile(regexZipcode)

regexPhone = r'(\(\d{3}\) {1}\d{3}-\d{4})+?'
regexPhone = re.compile(regexPhone)

#might need to escape forward slashes before turning in
regexWebsite= r'([a-zA-Z0-9_-]+\.com)</a>\s*</div>'
regexWebsite= re.compile(regexWebsite)

# make a dictionary of necessary attributes out of each url
def scrapUrl(url):
    data = urllib2.urlopen(url).read()
    dictionaryAttributes = {}
    nameMatch = regexName.search(data)
    streetMatch = regexStreet.search(data)
    cityMatch = regexCity.search(data)
    stateMatch = regexState.search(data)
    zipMatch = regexZipcode.search(data)
    phoneMatch = regexPhone.search(data)
    websiteMatch = regexWebsite.search(data)
    dictionaryAttributes['name'] = SpanOrNone(data, nameMatch, 0)
    dictionaryAttributes['street'] = SpanOrNone(data, streetMatch, 0)
    dictionaryAttributes['city'] = SpanOrNone(data, cityMatch, 1)
    dictionaryAttributes['state'] = SpanOrNone(data, stateMatch, 0 )
    dictionaryAttributes['zip'] = SpanOrNone(data, zipMatch, 0 )
    dictionaryAttributes['phone'] = SpanOrNone(data, phoneMatch, 0)
    dictionaryAttributes['website'] = SpanOrNone(data, websiteMatch, 0)
    return dictionaryAttributes

#this functions returns what the match found
# if the match found nothing, it returns 'NA'
def SpanOrNone(data, match, groupindex):
    if match==None:
        return 'NA'
    else:
        return match.groups()[groupindex]

dictionaries = [scrapUrl(url) for url in listOfUrls]

print '\n'

# human readable
for d in dictionaries:
    print 'Name: {0}'.format(d['name'])
    print 'Street Address: {0}'.format(d['street'])
    print 'City: {0}'.format(d['city'])
    print 'State: {0}'.format(d['state'])
    print 'Zip: {0}'.format(d['zip'])
    print 'Phone: {0}'.format(d['phone'])
    print 'Website: {0}'.format(d['website'])
    print '\n'
