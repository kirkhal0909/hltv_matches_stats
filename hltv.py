import requests

def parse(text,leftBlock,rightBlock,pos=0):
    leftPos = text.find(leftBlock,pos)
    if leftPos == -1:
        return ''
    leftPos += len(leftBlock)
    rightPos = text.find(rightBlock,leftPos)
    if rightPos == -1:
        return ''
    return text[leftPos:rightPos]

def getTeamStatsHLTV(link='https://www.hltv.org/stats/teams/matches/4494/mousesports'):
    request = requests.get(link)
    info = request.content
    '''
    file = open('matches.txt','wb')
    file.write(request.content)
    file.close()

    file = open('matches.txt','rb')
    info = file.read()
    file.close()
    '''

    data = []

    startBlock = b'td class="time'
    pos = info.find(startBlock)
    while pos != -1:    
        block = parse(info,startBlock,b'</tr',pos)[5:]
        #print(block)
        date = parse(block,b'>',b'<')
        block = block[block.find(b'class="flag"'):]
        team = parse(block,b'>',b'<')
        mapPlayed = parse(block,b'<span>',b'</span>')
        stats = parse(block,b'<span class="statsDetail">',b'<')
        block = block[block.find(b'<td class="text-center'):]
        win = parse(block,b'>',b'<')
        append = [date,team,mapPlayed,stats,win]
        data.append(append)
        pos += 1
        pos = info.find(startBlock,pos)
    data = [[element.decode() for element in block] for block in data]
    return data

def winLoseRateRange(data,dataRange = 0,playedMap = ''):
    if dataRange == 0:
        dataRange = len(data)
    dataRange = min(dataRange,len(data))
    print('\n\nLast',dataRange,'games winRate')
    win = 0
    lose = 0
    tie = 0
    for pos in range(dataRange):
        info = data[pos]
        if not playedMap or playedMap == info[2]:
            if info[4] == 'W':
                win += 1
            elif info[4] == 'L':
                lose += 1
            elif info[4] == 'T':
                tie += 1
            else:
                print(info)
    played = win+lose+tie
    winRate = format((win+tie)/played*100,'.2f')
    print('games:',str(played)+';\t','win:',str(win)+';\t','lose:',str(lose)+';\t','tie:',tie)
    print('win rate:',winRate+'%')
    return([played,win,lose,tie,winRate])

def winLoseRate(data,playedMap='Dust2'):
    packed = []
    packed.append(winLoseRateRange(data,10))
    packed.append(winLoseRateRange(data,100))
    packed.append(winLoseRateRange(data))
    packed.append(winLoseRateRange(data,0,playedMap))
    return packed

def allSteps(links,playedMaps=['Dust2']):
    packeds = []
    for link in links:
        print(link)
        data = getTeamStatsHLTV(link)
        for playedMap in playedMaps:
            print(playedMap)
            packeds.append(winLoseRate(data,playedMap))
            
        print('-------------------------------------')
        print()
    mapsOn = 3
    for column in range(len(packeds[0])):
        if column >= mapsOn:
            print(playedMaps[column-mapsOn])
        for packed in range(len(packeds)):
            print(links[packed])
            print(packeds[packed][column])
        print()

links = ['https://www.hltv.org/stats/teams/matches/4494/mousesports',
'https://www.hltv.org/stats/teams/matches/8474/100-thieves']
playedMaps = ['Dust2']

allSteps(links,playedMaps)

#Date opponent Map Result Win
