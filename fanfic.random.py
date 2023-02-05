# Today I learned that fanfic IDs as assingned sequentialy...
from random import choices as choices
import random 
import getFandomList 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

recentWorks = 'https://archiveofourown.org/works'

def workURL(num):
    return 'https://archiveofourown.org/works/{}'.format(num)

def getSoup(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup

def getNewest():
    newWorks = getSoup(recentWorks)
    return int(newWorks.find('ol', {'class': 'work index group'}).findAll('h4', {'class': 'heading'})[0].find('a')['href'].split('/works/')[1])

def getRandSingleWork():
    return getSoup(workURL(random.randint(1, getNewest())))

def singleWorkStats(soup, stats = 'all'):
    if type(stats) == list:
        ''
    elif stats == 'all':
        stats = ['published', 'status', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits']
    else:
        stats = [stats]

    statblock = soup.find('dl', {'class': 'stats'})

    returnList = []

    
    for stat in stats:
        try:
            term = statblock.find('dd', {'class': stat}).text
            try:
                returnList.append(int(term))
            except:
                if '/' in term:
                    returnList.append(int(term.split('/')[0]))
                if '-' in term:
                    returnList.append(term)
        except:
            if stat == 'status':
                returnList.append('Oneshot')
            else:
                returnList.append('ERROR')
                print(stat)
        
    return returnList

def singleWorkTags(soup, tags = 'all'):
    if type(tags) == list:
        ''
    elif tags == 'all':
        tags = ['rating', 'warning', 'category', 'fandom', 'relationship', 'character', 'freeform', 'language']
    else:
        tags = [tags]

    returnList = []
    for tag in tags:
        try:
            if tag == 'language':
                returnList.append([soup.find('dd', {'class', tag}).text.split('\n')[1].strip()])
            else:
                returnList.append([each.find('a').text for each in soup.find('dd', {'class': tag}).findAll('li')])
            
        except:
                print(tag)
                returnList.append('ERROR')

    return returnList

print(singleWorkTags(getSoup('https://archiveofourown.org/works/30257892')))