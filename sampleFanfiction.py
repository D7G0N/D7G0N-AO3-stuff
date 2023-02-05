# Will have functions for getting random samples of fanfiction to work with.
# Should be customizeable. 

from random import choices as choices
import random 
import getFandomList 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

# Get fandom list
    # Sort by work count
    # need two seperate lists: links and work counts 

def getFandoms(run = False):
    if run:
        getFandomList.main()
    allFandomsFile = open('allFandoms.csv', 'r', encoding='utf8')
    allFandoms = allFandomsFile.readlines()
    allFandomsFile.close()
    fandoms = []
    for fandom in allFandoms:
        properties = fandom.split(",")
        fandoms.append(properties)
    return fandoms

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

# Select fandoms
    # used weighted random
    # if fandom selected has less than ten works choose following fandoms to round it out
        # unless the parameter gets changed

def chooseFandoms(fandoms, howMany):
    workCounts = getWorkCounts(fandoms)
    fandomsChosen = choices(range(len(fandoms)), weights=workCounts, k = howMany)
    return fandomsChosen



# Select works
    # sort works by some parameter <- make changeable
    # maybe let it be able to choose filters?
    # choose random page and grab all ten fics
        # or grab only one, make this changeable
    # don't get locked out 


def generateUrl(fandoms, lookUp, sort, pageNum = 1):
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
    fandomNameUrl = fandoms[lookUp][0].split("/")[2]
    url = "https://archiveofourown.org/tags/{}/works?commit=Sort+and+Filter&page={}&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D={}&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=".format(fandomNameUrl, pageNum, sortUrl)
    return url

def choosePage(fandoms, lookup, sort):
    workCounts = getWorkCounts(fandoms)
    worksInFandom = workCounts[lookup]
    if worksInFandom < 10:
        return generateUrl(fandoms, lookup, sort)
    if worksInFandom >= 10:
        page = random.random() * (worksInFandom / 20)
        page = int(page)
        return generateUrl(fandoms, lookup, sort, page)


def getStat(url, statType, term = ''):
    '''statType = words, chapters, comments, kudos, bookmarks, hits, ifTag'''
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find("ol", {"class":"work index group"}).findChild().findNextSiblings()
    containers.insert(0, page_soup.find("ol", {"class":"work index group"}).findChild())
    #print(len(containers))

    stats = []
    for work in containers:
        statblock = work.find('dl', {'class': 'stats'}) 
        try:
            match statType:
                case "words":
                    stat = statblock.find("dd", {"class": 'words'})
                    split = stat.text.split(',')
                    stat = ''.join(split)
                    stat = int(stat)
                case "ifTag":
                    tags = work.find("ul", {"class": 'tags commas'})
                    textTags = []
                    for tag in tags:
                        tagText = tag.text
                        tagText = tagText.replace('\n', '')
                        if tagText != ' ' and tagText != '':
                            textTags.append(tagText)
                    if term in textTags:
                        stat = True
                    else:
                        stat = False
                case 'mentions':
                    total = 0
                    tags = work.find("ul", {"class": 'tags commas'})
                    textTags = []
                    for tag in tags:
                        tagText = tag.text
                        if term in tagText:
                            total += 1
                    block = work.find('blockquote', {'class': 'userstuff summary'})
                    block = block.findChild().text
                    total += block.count(term)
                    stat = total
                case 'numTags':
                    tags = work.find("ul", {"class": 'tags commas'})
                    textTags = []
                    for tag in tags:
                        tagText = tag.text
                        tagText = tagText.replace('\n', '')
                        if tagText != ' ' and tagText != '':
                            textTags.append(tagText)
                    stat = len(textTags)
                case _ :
                    statHolder = statblock.find("dd", {"class": statType})
                    stat = statHolder.contents[0]
                    stat = int(stat.text)
            stats.append(stat)
        except:
            stats.append(0)
            # print('x', end = '')
    return stats
    

def loading(num, total):
    bar = int((num / total) * 10)
    return '\n'*7 + '[' + '-'*bar + '>' + ' '*(10 - bar) + ']'
# Get data from works
    # make this changeable
    # 

def getSample(stat1, stat2 = 0, stat3 = 0, sampleSize = 10, sort = 'title', run = False):
    '''stat: words, chapters, comments, kudos, bookmarks, hits
    sort: author, title, date posted, date updated, word count, hits, kudos, comments, bookmarks'''
    fandoms = getFandoms(run)
    fandomsChosen = chooseFandoms(fandoms, sampleSize)
    allStats1 = []
    allStats2 = []
    allStats3 = []
    loop = 0
    length = len(fandomsChosen)
    for lookup in fandomsChosen:
        print(loading(loop, length))
        url = choosePage(fandoms, lookup, sort)
        pageStats = getStat(url, stat1)
        allStats1 += pageStats
        if stat2 != 0 :
            pageStats = getStat(url, stat2)
            allStats2 += pageStats
        if stat3 != 0 :
            pageStats = getStat(url, stat3)
            allStats3 += pageStats
        loop += 1
    return allStats1, allStats2, allStats3
