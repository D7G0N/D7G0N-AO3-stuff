import AO3ScraperTools as tools

def readSidebar(soup, tags = 'all'):
    if tags == 'all':
        tags = ['rating', 'warning', 'category', 'fandom', 'character', 'relationship', 'freeform']
    if type(soup) == str:
        soup = tools.getSoup(soup)
    if type(tags) != list:
        return 'ERROR: tags is not a list'
    
    sidebar = {}
    for tagType in tags:
        if tagType == 'warning':
            tagType = 'archive_warning'

        dropdown = soup.find('dd', {'id': 'include_{}_tags'.format(tagType)}).findAll('li')
        for each in dropdown:
            tagNameCount = each.findAll('span')[1].text.split(' (')
            tagCount = tools.cleanParentheses(tagNameCount.pop(-1))
            tagName = ' ('.join(tagNameCount)
            sidebar[tagName] = int(tagCount)

    return sidebar

url = 'https://archiveofourown.org/tags/%E5%83%95%E3%81%AE%E3%83%92%E3%83%BC%E3%83%AD%E3%83%BC%E3%82%A2%E3%82%AB%E3%83%87%E3%83%9F%E3%82%A2%20%7C%20Boku%20no%20Hero%20Academia%20%7C%20My%20Hero%20Academia/works'
soup = tools.getSoup(url)
print(readSidebar(soup))