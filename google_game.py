from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
  
def bs_open(url):
    html=urlopen(url)
    try:
        return BeautifulSoup(html)
    except TypeError as e:
        print('Error : '+str(e))
        print('None obj will be returned')
        return None

def getGameCategory(main_url):
    '''
    Get the main google play game link
    and return the list of category-links
    '''
    clinks=[]
    address='/store/apps/category/GAME'
    soup=bs_open(main_url)
    links=soup.findAll('a',href=re.compile('^(/store/apps/category/)[A-Za-z_]+$'))
    for link in links:
        if link['href']==address:
            continue
        clinks.append(link['href'])
    return clinks

def scrapeCategory(page_link,limit=10):
    '''
    Get the Category page of games
    and write description of random games in file
    using gamepage_scrape
    limit - the number of games that would be scraped from Page
    '''
    page_url='https://play.google.com'+page_link
    soup=bs_open(page_url)
    gameList=soup.find('div',class_='id-card-list card-list two-cards').findChildren('div',
                            class_='card no-rationale square-cover apps small')
    random.shuffle(gameList)
    for game in gameList[:limit]:
        game_link=game.find('a',href=True).attrs['href']
        gamepage_scrape(game_link)
         

def gamepage_scrape(game_link):
    '''
    Get game title and description from game page
    and write them to 'Game_Description.txt'
    '''
    gamePage_url='https://play.google.com'+game_link
    soup=bs_open(gamePage_url)
    name=soup.find('div',class_='id-app-title').get_text()
    text=soup.find('div',class_='show-more-content text-body').get_text()
    print(name,file=writer)
    print('---------',file=writer)
    print(text,file=writer)
    print('\n\n\n',file=writer)


url='https://play.google.com/store/apps/category/GAME'
writer=open('Game_Description.txt','w')

categoryLinks=getGameCategory(url)
for link in categoryLinks:
    scrapeCategory(link,limit=2)

writer.close()
