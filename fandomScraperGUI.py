import PySimpleGUI as sg
import AO3ScraperTools as tools
import webbrowser

sg.theme('DarkRed1')  
'''main_layout = [  [sg.Text('url:'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Exit')] ]'''

main_layout = [
    [sg.Button('Any Work')],
    [sg.Button('Any Fandom')],
    [sg.Button('One Work')],
    [sg.Button('One Fandom')],
    [sg.Text('')],
    [sg.Text('\t\t\t'), sg.Button('Exit')],
]

anyWork_layout = [
    [sg.Text('Number of works:'), sg.InputText()],
    [sg.Text('Specify stats:'), sg.InputText(), sg.Button(key ='s_help', button_text= '?')],
    [sg.Text('Specify tags:'), sg.InputText(), sg.Button(key ='t_help', button_text= '?', )],
    [sg.Text('')],
    [sg.Text('Out file - stats:'), sg.Input(), sg.FileBrowse()],
    [sg.Text('Out file - tags:'), sg.Input(), sg.FileBrowse()],
    [sg.Text('')],
    [sg.ProgressBar(100, size = (50, 10), key = 'anyWork_progress', bar_color=('white', 'gray'))],
    [sg.Text('')],
    [sg.Button('Run'), sg.Button('Exit')],
]

def anyWork_code():
    while True:
        event, values = main.read()
        match event:
            case sg.WIN_CLOSED:
                break
            case 'Exit':
                break
            case 't_help':
                webbrowser.open('https://docs.google.com/document/d/1T5VoicCs4dhrbNsZoiUq7FWEBogqK5xEhVUonMwMm3k/edit?usp=sharing')
            case 's_help':
                webbrowser.open('https://docs.google.com/document/d/1T5VoicCs4dhrbNsZoiUq7FWEBogqK5xEhVUonMwMm3k/edit?usp=sharing')
            case 'Run':
                if values[0] == '':
                    values[0] = 1
                for each in range(int(values[0])):
                    progress = (each / int(values[0])) * 100
                    main['anyWork_progress'].update(int(progress))
                    
                    work = tools.getRandSingleWork()
                    with open(values[3], 'a', encoding='utf8') as stats:
                        if work.find('h2', {'class': 'title heading'}) == None:
                            stats.write("'Private Work' \n")
                            continue
                        if ',' in values[1]:
                            values[1] = values[1].split(', ')
                        if values[1] == 'none':
                            continue
                        stats.write(str(tools.workStats(work, values[1]))[1:-1] + '\n')
                        
                    with open(values[4], 'a', encoding='utf8') as tags:
                        if work.find('h2', {'class': 'title heading'}) == None:
                            tags.write("'Private Work' \n")
                            continue
                        if ',' in values[2]:
                            values[2] = values[2].split(', ')
                        if values[2] == 'none':
                            continue
                        if work.find('p', {'class': 'caution'}) != None:
                            tags_list = tools.workOnPageTags(work, values[2])
                        else:
                            tags_list = tools.singleWorkTags(work, values[2])
                        tags.write(tools.reorderTags(tags_list))
                    
                main['anyWork_progress'].update(100)
                print('done')


main = sg.Window('AO3 Scraper', main_layout)
while True:
    event, values = main.read()
    match event:
        case sg.WIN_CLOSED:
            break
        case 'Exit':
            break
        case 'Any Work':
            main.close()
            main = sg.Window('AO3 Scraper - Any Work', anyWork_layout)
            anyWork_code()
        case 'Any Fandom':
            ''
        case 'One Work':
            ''
        case 'One Fandom':
            ''
main.close()