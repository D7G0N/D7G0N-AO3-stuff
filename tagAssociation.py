import AO3ScraperTools as tools
MINWORKS = 100000

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

with open('temp.txt', 'r') as temp_file:
    temp = [int(each.strip('\n')) for each in temp_file.readlines()]

if len(temp) != 2:
    temp = [0,0]

if temp[0] == 0:
    with open("tagsDatabase.csv", 'r', encoding='utf8') as file:
        tagsRaw = file.readlines()
    allTags = string_dict(tagsRaw)

    bigTags = {}
    count = 0
    for tag in allTags:
        if int(allTags[tag][1]) >= MINWORKS :
            bigTags[tag] = allTags[tag] + [count]
            count += 1

    count = len(bigTags)
    print(count)
    temp[1] = count

    with open('crossTags.csv', 'w', encoding= 'utf8') as file:
        headers = ';' + ';'.join([tag for tag in bigTags]) + '\n'
        file.write(headers)

num = temp[0]

for tag in bigTags:
    line = [0] * count

    name = tag
    print(name)
    url = tag_url(tag)
    try:
        crossovers = tools.readSidebar(url, ['relationship', 'character', 'freeform'])
        #print(sidebar)
        if type(crossovers) == int:
            print(crossovers)
    except:
        temp[0] = bigTags[tag][2]
        with open('temp.txt', 'w') as temp_file:
            temp_file.write("\n".join([str(each) for each in temp]))
        print("HTTP Error 429: Too Many Requests")
        break

    for over in crossovers:
        try: 
            cross_idef = bigTags[over][2]
            line[cross_idef] = crossovers[over]
            
        except:
            ''
    
    line = str(name) + ';' + ';'.join([str(weight) for weight in line]) + '\n'
    #print(line)
    with open('crossTags.csv', 'a', encoding= 'utf8') as file:
        file.write(line)

    num += 1

temp = [0, 0]
with open('temp.txt', 'w') as temp_file:
    temp_file.write("\n".join([str(each) for each in temp]))
