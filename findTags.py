import AO3ScraperTools as tools

def tag_url(tag):
    tag = tag.replace(" ", "%20")
    tag = tag.replace("/", "*s*")
    tag = tag.replace("|", "%7c")
    tag = tag.replace("&", "*a*")
    tag = tag.replace('.', "*d*")
    url = 'https://archiveofourown.org/tags/{}/works'.format(tag)
    return url

def string_dict(string):
    tags = {}
    for tagLine in string:
        tagLine = tagLine.replace("\n", "")
        tagSplit = tagLine.split(", ")
        tagSplit[2] = int(tagSplit[2])
        tags[tagSplit[0]] = tagSplit[1:3]
    return tags

def newTags(numworks):
    fandoms = tools.getFandoms()
    workCounts = tools.getWorkCounts(fandoms)
    with open("tagDataBaseRaw.csv", 'a', encoding = 'utf8') as file:
        lookup = tools.chooseFandoms(fandoms, workCounts, 1)[0]
        try:
            soup = tools.getSoup(tools.choosePage(fandoms, workCounts, lookup))
            if type(soup) == int:
                return numworks, 0
        except:
            print('HTTP Error 429: Too Many Requests')
            return numworks, 1
        worksonpage = soup.findAll('li', {'role': 'article'})
        for work in worksonpage:
            for tagtype in ['relationship', 'character', 'freeform']:
                tagsonpage = tools.workOnPageTags(work, tagtype)[0]
                for tag in tagsonpage:
                    line = tag + ", " + tagtype + "\n"
                    file.write(line)
            numworks += 1
            #print(numworks, end = ', ')
    return numworks, 0

def findSameTag():
    with open("tagsDatabase.csv", 'r', encoding='utf8') as file:
        tagsRaw = file.readlines()
    allTags = string_dict(tagsRaw)
    allTagsNew = allTags.copy()
    for tagi in allTags:
        loweri = tagi.lower()
        counti = allTags[tagi][1]
        for tagj in allTags:
            lowerj = tagj.lower()
            countj = allTags[tagj][1]
            if len(str(counti)) > 4:
                counti = round(counti, 4 - len(str(counti)))
                countj = round(countj, 4 - len(str(countj)))
            if loweri != lowerj and counti == countj and counti > 5 and lowerj in loweri:
                if (("|" in tagi and "|" not in tagj)  or ("(" in tagi and "(" not in tagj)) and 'mentioned' not in tagi:
                    print(tagj, end=";\t\t\t\t")
                    print(tagi)
                    try:
                        del allTagsNew[tagj]
                    except:
                        ''
                else:
                    print(tagi, end=";\t\t\t\t")
                    print(tagj)
                    try:
                        del allTagsNew[tagi]
                    except:
                        ''
    with open("tagsDatabase.csv", 'w', encoding='utf8') as file:
        for tag in allTagsNew:
            line = tag + ", "+ allTags[tag][0] + ", " + str(allTags[tag][1]) + "\n"
            file.write(line)
        print('Done')

def knownTags(newworks):
    with open("knownTags.csv", 'r', encoding='utf8') as file:
        bigTagsRaw = file.readlines()
        knownWorks = bigTagsRaw.pop(0)
        knownWorks = int(knownWorks.split(' ')[1])

    bigTags = string_dict(bigTagsRaw)
    
    with open('tagDataBaseRaw.csv', 'r', encoding='utf8') as file:
        newTagsRaw = file.readlines()
    newTags = []
    for tagLine in newTagsRaw:
        tagLine = tagLine.replace("\n", "")
        newTags.append(tagLine.split(", "))

    for tag in newTags:
        if tag[0] in bigTags:
            bigTags[tag[0]][1] += 1
        else:
            bigTags[tag[0]] = [tag[1], 1]

    #print(bigTags)
    with open("knownTags.csv", 'w', encoding='utf8') as file:
        #print(str(knownWorks) + str(newworks))
        line = 'Works: ' + str(knownWorks + newworks) + '\n'
        file.write(line)
        for tag in bigTags:
            line = tag + ", "+ bigTags[tag][0] + ", " + str(bigTags[tag][1]) + "\n"
            file.write(line)

def tag_count(name, url = 0):
    if url == 0:
        url = tag_url(name)
        #print(url)
    soup = tools.getSoup(url)
    if type(soup) == int:
        print('Error', end= ' ')
        match soup:
            case 429:
                print('HTTP Error 429: Too Many Requests')
                return -1
            case 404:
                print(soup)
                print(name, end=': ')
                print(url)
                return 0
            case _:
                print(soup)
                print(name, end=': ')
                print(url)
                return -2
    try:
        check = soup.findAll('a', {'class': 'tag'})
        check = check[0] 
        count = check.parent.text
        count = count.split(' ')[7].replace(',', '')
        count = int(count)
        return count
    except:
        print(name, end=': ')
        print(url)
        return 0

def true_tags(count, minWorks = 5, reset = False):
    if reset:
        with open("tagsDatabase.csv", 'w', encoding='utf8') as file:
            file.write('')
    
    with open("knownTags.csv", 'r', encoding='utf8') as file:
        knownTagsRaw = file.readlines()
        knownWorks = knownTagsRaw.pop(0)
        knownWorks = int(knownWorks.split(' ')[1])

    knownTags = string_dict(knownTagsRaw)

    with open("tagsDatabase.csv", 'r', encoding='utf8') as file:
        trueTagsRaw = file.readlines()

    trueTags = string_dict(trueTagsRaw)

    for tag in knownTags:
        if count <= 0:
            break
        
        contents = knownTags[tag]
        if tag not in trueTags and contents[1] >= minWorks:
            contents[1] = tag_count(tag)
            trueTags[tag] = contents
           
            match contents[1]:
                case -1:
                    break
                case 0:
                    continue
            
            print(count, end='; ')
            print(tag)
            count -= 1
    if count > 0 :
        print("FINISHED!!!")
        return True

    with open("tagsDatabase.csv", 'w', encoding='utf8') as file:
        for tag in trueTags:
            line = tag + ", "+ trueTags[tag][0] + ", " + str(trueTags[tag][1]) + "\n"
            file.write(line)
        print('Done')
    return False

def doublecheck():
    with open("tagsDatabase.csv", 'r', encoding='utf8') as file:
        trueTagsRaw = file.readlines()
    trueTags = string_dict(trueTagsRaw)

    for tag in trueTags:
        contents = trueTags[tag]
        if contents[1] == -2:
            contents[1] = tag_count(tag)
            print(tag)
            print(contents[1])
            trueTags[tag] = contents
        match contents[1]:
            case -1:
                break
            case 0:
                continue
        
        

        #print(count, end='; ')
        #print(tag)
        #count -= 1

    with open("tagsDatabase.csv", 'w', encoding='utf8') as file:
        for tag in trueTags:
            line = tag + ", "+ trueTags[tag][0] + ", " + str(trueTags[tag][1]) + "\n"
            file.write(line)
        print('Done')

def randomTagsPage(count):
    for each in range(count):
        url = 'https://www.google.com/webhp?hl=en&sa=X&ved=0ahUKEwjwjtytyPr8AhVAlIkEHVWBCIoQPAgD'
        soup = tools.getSoup(url)
        url = "https://archiveofourown.org/tags?show=random"
        soup = tools.getSoup(url)
        cloud = soup.find('ul', {'class': 'tags cloud index group'})
        tags = [tag.find('a').text for tag in cloud.findAll('li')]
        sizes = [tag.find('a')['class'] for tag in cloud.findAll('li')]
        #print(sizes)
        sizes = [int(size[0].strip('cloud')) for size in sizes]
        for i in range(len(tags)):
            #count = tag_count(tags[i])
            line = str(tags[i]) + ", " + str(sizes[i]) + "\n"
            with open('freeformsRaw.csv', 'a', encoding='utf-8') as file:
                file.write(line)
            print(tags[i])

""""
Cloud Count:
1:  1 -   5
2:  6 -   25
3:  26 -  """


def main1(count):
    newworks = 0
    #count = int(input('Number of pages to scrape: '))
    while count > 0:
        newworks, error = newTags(newworks)
        if error == 1:
            break
        print(count)
        count -= 1

    knownTags(newworks)
    print('Proccessed Successfully')

    with open('tagDataBaseRaw.csv', 'w') as file:
        file.write('')

def main2(repeats):
    count = repeats * 25
    for each in range(repeats):
        done = true_tags(25)
        if done:
            break
        print("-------------- {} --------------".format(repeats - each))
    doublecheck()
    return done

def main3(times):
    for each in range(times):
        main1(10)
        while main2(1) == 0:
            ''
        print("---------- REPEAT #{} ----------".format(each))
        

#true_tags(1000)
#doublecheck()
#main2(10)
main3(100)
#findSameTag()
