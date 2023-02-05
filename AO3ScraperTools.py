'''
This file is the masterlist of the better functions I've written for scraping info from AO3
I wrote the comments. Hopefully without breaking anything in the proccess. 
I also did edits for consistency and haven't debugged them yet, so...
'''

from random import choices as choices
import random 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib3

# reads a webpage and parses it into BeautifulSoup4
def getSoup(url):
    try:
        #uClient = uReq(url)
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
    except:
        http = urllib3.PoolManager()
        error = http.request("GET", url)
        match error.status:
            case 404:
                return 404
            case 200:
                #print(error)
                return 200
            case _ :
                print(error.status)
                return(0)

    '''http = urllib3.PoolManager()
    uClient = http.request("GET", url)
    match uClient.status:
        case 404:
            return 404
        case 200:
            print(uClient.status)
            #return 200
        case _ :
            print(uClient.status)
            return(0)'''
    page_html = resp.data #.decode('utf-8')
    #page_html = uClient.read()
    #uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup

# unpacks the file fandomGroups.csv into a list
def getFandomGroups(f_in):
    fandomGroups = []
    for line in f_in:
        group = line.split(", ")
        fandomGroups.append(group)
    return fandomGroups

# gets the parenthesies off a string
def cleanParentheses(string):
    index = string.find('(')
    index += 1
    index2 = string.find(')')
    index2 -= 0
    return string[index:index2]

# make a list of all the fandoms on AO3
def getFandomList():

    # unpacks the file fandomGroups.csv into a list
    with open('fandomGroups.csv', 'r') as f_in:
        fandomGroups = getFandomGroups(f_in)
    
    # opens a new file to write all the fandoms to
    filename = "allFandoms.csv"
    f_out = open(filename, "w", encoding='utf8')  

    # reads each fandom category page on AO3
    for group in fandomGroups:
        # retrives the url for the fandom category page 
        print(group[0])
        group_url = group[1]  
        group_url = group_url.replace('\n', '')

        # gets the soup 
        page_soup = getSoup(group_url)

        # each container is a fandom on the fandom category page
        containers = page_soup.findAll("a",{"class":"tag"})

        # gets the name of and link to every fandom in the category
        for container in containers:
            fandomName = container.text
            fandomLink = container.get('href')
            fandomWorks = container.next_sibling
            fandomWorks = cleanParentheses(fandomWorks)

            # writes the link, name, category, and number of works for each fandom to 'allFandoms.csv'
            line = str(fandomLink) + ', ' + str(fandomName) + ', ' + str(group[0]) + ', ' + str(fandomWorks) + "\n"
            f_out.write(line)

    f_out.close()

# unpacks the file 'allFandoms.csv' into a list of lists
# each sublist containing the href, fandom name, fandom group, and a \n
def getFandoms(run = False):
    # has the option of refreshing/updating 'allFandoms.csv' before use
    if run:
        getFandomList()

    # turns each line in the file into an element in a list
    with open('allFandoms.csv', 'r', encoding='utf8') as allFandomsFile: 
        allFandoms = allFandomsFile.readlines()

    # splits each element in allFandoms into a list, such that new list fandoms is a list of lists
    fandoms = []
    for fandom in allFandoms:
        properties = fandom.split(",")
        fandoms.append(properties)
    return fandoms

# puts just the work counts from the list of lists from 'allFandoms.csv' into their own list
def getWorkCounts(fandoms):
    workCounts = []
    for fandom in fandoms:
        try:
            works = fandom[3].split('\n')[0]
            works = int(works)
        except:
            works = 1
        workCounts.append(works)
    return workCounts

# samples fandoms, with weights based on work count, but only returns their indecies in the all fandoms list
def chooseFandoms(fandoms, workCounts, howMany):
    fandomsChosen = choices(range(len(fandoms)), weights=workCounts, k = howMany)
    return fandomsChosen

# creates a url based a fandom's index in the allFandoms list, that leads to a page of the works in that 
# fandom, with options to specify the sort or go to a certain page.  
def generatePageUrl(fandoms, lookUp, sort = 'date updated', pageNum = 1):
    
    # translates sort types from how they are know to how they appear in the soup
    sortTypes = {
        'author': 'authors_to_sort_on',
        'title': 'title_to_sort_on',
        'date posted': 'created_at',
        'date updated': 'revised_at',
        'word count': 'word_count',
        'hits': 'hits',
        'kudos': 'kudos_count',
        'comments': 'comments_count',
        'bookmarks': 'bookmarks_count',
    }
    sortUrl = sortTypes[sort]

    # finds the correct way to refer to the fandom in a url
    fandomNameUrl = fandoms[lookUp][0].split("/")[2]
    # formats the url
    url = "https://archiveofourown.org/tags/{}/works?commit=Sort+and+Filter&page={}&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D={}&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=".format(fandomNameUrl, pageNum, sortUrl)
    return url

# returns the url of a random page in the search results for a fandom
def choosePage(fandoms, workCounts, lookup, sort = 'date updated'):
    worksInFandom = workCounts[lookup]
    # there are 20 works on each result page, so a random page must be chosen between 1 and works divided by 20,
    # plus the page with less than 20 works on it.
    if worksInFandom < 20:
        return generatePageUrl(fandoms, lookup, sort)
    if worksInFandom >= 20:
        page = random.randint(1, int(worksInFandom / 20) + 1)
        return generatePageUrl(fandoms, lookup, sort, page)

# creates a url for a specific work based on its AO3 assinged number
def workURL(num):
    url = 'https://archiveofourown.org/works/{}'.format(num)
    print(".")
    return url

# gets the assinged number of the newest work on AO3
def getNewest():
    newWorks = getSoup('https://archiveofourown.org/works')
    return int(newWorks.find('ol', {'class': 'work index group'}).findAll('h4', {'class': 'heading'})[0].find('a')['href'].split('/works/')[1])

# returns the url of a random single work
def getRandSingleWork():
    while True:
        try:
            soup = getSoup(workURL(random.randint(1, getNewest())))
            break
        except:
            continue
    return soup

# reads the stats for a work on AO3
# soup is soup - this can be the entire page for a single work, or a slice of a search page.
def workStats(soup, stats = 'all'):
    # makes sure that stats is a list of all the stats to find, even if the list only has a single element.
    if type(stats) == list:
        ''
    elif stats == 'all' or stats == '':
        stats = ['url', 'published', 'status', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits']
    else:
        stats = [stats]

    # the part of the soup with the stats in it. 
    statblock = soup.find('dl', {'class': 'stats'})

    returnList = []
    for stat in stats:
        try:
            #find the stat
            term = statblock.find('dd', {'class': stat}).text
            try:
                if term == 'bookmarks':
                    term = statblock.find('dd', {'class': stat}).find('a').text
                #try to save it as an integer
                returnList.append(int(term))
            except:
                if '/' in term:
                    # if the stat is chapter/chapters, just save the number of chapters that actualy exist
                    returnList.append(int(term.split('/')[0]))
                if '-' in term:
                    # if the stat is a date, just save it as a string
                    returnList.append(term)
                if ',' in term:
                    # if the stat has a comma in it get rid of that comma 
                    returnList.append(int(term.replace(',', '')))
        except:
            if stat == 'status':
                # if a work doesn't have a status stat, it has never been updated, and is therefore a oneshot
                returnList.append('Oneshot')
            elif stat == 'published':
                    returnList.append(soup.find('p', {'class': 'datetime'}).text)
            elif stat == 'url':
                # how to find the url
                try:
                    share = soup.find('li', {'class': 'share'}).find('a')['href']
                except: 
                    try:
                        share = soup.find('h4', {'class': 'heading'}).find('a')['href']
                    except:
                        share = 'ERROR'
                share = share.replace('/share', '')
                returnList.append(share)
            elif stat == 'comments' or stat == 'kudos' or stat == 'hits' or stat == 'bookmarks':
                    returnList.append(0)
            else:
                # oh joy something went wrong, maybe if I print what stat I was on I can debug. 
                returnList.append('ERROR')
                print(stat)
        
    return returnList

# reads the stats for a work on its own page on AO3
# soup now comes in flavors, formating is different on page with many works
def singleWorkTags(soup, tags = 'all'):
    # makes sure that tags is a list of all the stats to find, even if the list only has a single element.
    if type(tags) == list:
        ''
    elif tags == 'all' or tags == '':
        tags = ['rating', 'warning', 'category', 'fandom', 'relationship', 'character', 'freeform', 'language']
    else:
        tags = [tags]

    # append each tag we find to a list so we can return them all at once
    returnList = []
    for tag in tags:
        try:
            if tag == 'language':
                # the tag 'language' can be found here:
                returnList.append([soup.find('dd', {'class': tag}).text.split('\n')[1].strip()])
            else:
                # all other tags can be found here:
                returnList.append([each.find('a').text for each in soup.find('dd', {'class': tag}).findAll('li')])
            
        except:
            if tag == 'relationship':
                returnList.append(['no relationship'])
            # yay error message.
            print(tag)
            returnList.append(['ERROR'])

    return returnList

# reads the stats for a work on a page with many works on AO3
# soup now comes in flavors, formating is different on page with many works
def workOnPageTags(soup, tags = 'all'):
     # makes sure that tags is a list of all the stats to find, even if the list only has a single element.
    if type(tags) == list:
        ''
    elif tags == 'all' or tags == '':
        tags = ['rating', 'warning', 'category', 'fandom', 'relationship', 'character', 'freeform', 'language']
    else:
        tags = [tags]

     # append each tag we find to a list so we can return them all at once
    returnList = []
    for tag in tags:
        # the are where tags are varies based on type of tag.
        if tag in ('fandom', 'rating', 'warning', 'category', 'complete'):
            tagblock = soup.find('div', {'class': 'header module'}) 
        else:
            # warnings, relationships, characters, freeforms, language
            tagblock = soup.find('ul', {'class': 'tags commas'})
        
        
        try:
            # this is where you can find each of the different kinds of tags! In like 5 differnt places!
            match tag:
                case 'fandom':
                    returnList.append([each.text for each in tagblock.find('h5').findAll('a')])
                case 'rating':
                    returnList.append([tagblock.find('ul').findAll('li')[0].find('a').find('span')['title']])
                case 'warning':
                    returnList.append([tagblock.find('ul').findAll('li')[1].find('a').find('span')['title']])
                case 'category':
                    returnList.append(tagblock.find('ul').findAll('li')[2].find('a').find('span')['title'].split(', '))
                case 'complete':
                    returnList.append([tagblock.find('ul').findAll('li')[3].find('a').find('span')['title']])
                case 'warnings':
                    returnList.append([each.find('strong').find('a').text for each in tagblock.findAll('li', {'class': 'warnings'})])
                case 'language':
                    returnList.append([soup.find('dd', {'class', 'language'}).text])
                case 'relationship':
                    returnList.append([each.find('a').text for each in tagblock.findAll('li', {'class': 'relationships'})])
                case 'character':
                    returnList.append([each.find('a').text for each in tagblock.findAll('li', {'class': 'characters'})])
                case 'freeform':
                    returnList.append([each.find('a').text for each in tagblock.findAll('li', {'class': 'freeforms'})])
                
                case _ :   
                    returnList.append(['ERROR'])
        except:
            if tag == 'relationship':
                returnList.append(['no relationship'])
            print(tag)
            returnList.append(['ERROR'])
    return returnList

# reads the stat names and respective work counts as shown on the sidebar
def readSidebar(soup, tags = 'all'):
    if tags == 'all':
        tags = ['rating', 'warning', 'category', 'fandom', 'character', 'relationship', 'freeform']
    if type(soup) == str:
        soup = getSoup(soup)
        if type(soup) == int:
            return soup
    if type(tags) != list:
        return 'ERROR: tags is not a list'
    
    sidebar = {}
    for tagType in tags:
        if tagType == 'warning':
            tagType = 'archive_warning'

        dropdown = soup.find('dd', {'id': 'include_{}_tags'.format(tagType)}).findAll('li')
        for each in dropdown:
            tagNameCount = each.findAll('span')[1].text.split(' (')
            tagCount = cleanParentheses(tagNameCount.pop(-1))
            tagName = ' ('.join(tagNameCount)
            sidebar[tagName] = int(tagCount)

    return sidebar

# takes a list of list of tags and turns it into a string for a csv such that 
# each type of tag gets its own column and each column is of variable length
def reorderTags(tags):
    lines = ''
    max = 0

    # finds the length of the tag category with the most tags in it. 
    # this length is the number of rows we need
    for each in tags:
        if type(each) == list:
            if len(each) > max:
                max = len(each)
    
    # goes row by row, adding a tag for each category in each column 
    for each in range(0, max):
        for tag in tags:
            try: 
                lines += (tag[each] + ',')
            except:
                # if one kind of tag doesn't have any tags in this row, and an empty cell in its column
                lines += (',')
        lines += '\n'
    return lines

# prints a loading bar for pieces of code that take a long time.
def loading(num, total):
    bar = int((num / total) * 10)
    return '\n'*7 + '[' + '-'*bar + '>' + ' '*(10 - bar) + ']'


