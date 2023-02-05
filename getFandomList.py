#python3.9.exe 1.py
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

def getGroups(f_in):
    fandomGroups = []
    for line in f_in:
        group = line.split(", ")
        fandomGroups.append(group)
    return fandomGroups

def cleanWorks(Works):
    index = Works.find('(')
    index += 1
    index2 = Works.find(')')
    index2 -= 0
    return Works[index:index2]

def main():
    filename = "fandomGroups.csv"
    f_in = open(filename, "r")

    filename = "allFandoms.csv"
    f_out = open(filename, "w", encoding='utf8')

    fandomGroups = getGroups(f_in)
    f_in.close()

    for group in fandomGroups:
        print(group[0])
        group_url = group[1]  
        group_url = group_url.replace('\n', '')
        #print(group_url)
        
        uClient = uReq(group_url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("a",{"class":"tag"})
        #container = containers[0]

        for container in containers:
            #print(container)
            fandomName = container.text
            fandomLink = container.get('href')
            fandomWorks = container.next_sibling
            fandomWorks = cleanWorks(fandomWorks)
            line = str(fandomLink) + ', ' + str(fandomName) + ', ' + str(group[0]) + ', ' + str(fandomWorks) + "\n"
            #line = line.encode('utf-8')
            f_out.write(line)

    f_out.close()
