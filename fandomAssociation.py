import AO3ScraperTools as tools
MINWORKS = 10000

with open('temp.txt', 'r') as temp_file:
    temp = [int(each.strip('\n')) for each in temp_file.readlines()]

if len(temp) != 2:
    temp = [0,0]

if temp[0] == 0:
    fandoms = tools.getFandoms(run = False)
    idef_lookup = {}
    count = 0
    while count < len(fandoms):
        try:
            if int(fandoms[count][3]) < MINWORKS :
                fandoms.pop(count)
                continue
        except:
            fandoms.pop(count)
            continue
        fandoms[count][1] = fandoms[count][1].strip()
        idef_lookup[fandoms[count][1]] = count
        count += 1

    temp[1] = count

    with open('crossFandoms.csv', 'w', encoding= 'utf8') as file:
        headers = ';' + ';'.join([fandom[1] for fandom in fandoms ]) + '\n'
        file.write(headers)

num = temp[0]

while num <= temp[1]:
    fandom = fandoms[num]
    line = [0] * count

    name = fandom[1]
    print(name)
    idef = idef_lookup[name]
    url = tools.generatePageUrl(fandoms, idef)
    try:
        crossovers = tools.readSidebar(url, ['fandom'])
    except:
        temp[0] = num
        with open('temp.txt', 'w') as temp_file:
            temp_file.write("\n".join(temp))
        print("HTTP Error 429: Too Many Requests")
        break

    for over in crossovers:
        try: 
            cross_idef = idef_lookup[over]
            line[cross_idef] = crossovers[over]
            
        except:
            ''
    
    line = str(name) + ';' + ';'.join([str(weight) for weight in line]) + '\n'
    #print(line)
    with open('crossFandoms.csv', 'a', encoding= 'utf8') as file:
        file.write(line)

    num += 1

temp = [0, 0]
with open('temp.txt', 'w') as temp_file:
    temp_file.write("\n".join(temp))
