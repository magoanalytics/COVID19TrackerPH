import urllib
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.request import Request, urlopen


def get_abscbn():
    try:
        # Listing down all the news articles about COVID

        abs_ncov_news = []
        page_link = '/list/tag/2019-novel-coronavirus'
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0)'

        while page_link != False:
            req = Request('https://news.abs-cbn.com' + page_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'})
            content = urlopen(req).read()
            soup = BeautifulSoup(content)

            mydivs = soup.find("section", {'class':"section-more-stories"})

            mydivs = mydivs.find_all("p", {'class':"title"})

            abs_ncov_news += [url.a['href'] for url in mydivs] 
            time.sleep(6)

            try:
                page_link = soup.find("a", {'title':"Next"})['href']
            except:
                page_link = False

            abscbn_df = pd.DataFrame(columns = ['source_id','date','category','title','author','text'])


        # Scraping all the articles in the list
        
        df = pd.read_csv('scraped_data/abscbn_scraped.csv')
        article_list = list(df['title'].unique())

        for article in abs_ncov_news:  
            user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
            req = Request('https://news.abs-cbn.com' + article, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'})
            content = urlopen(req).read()
            soup = BeautifulSoup(content)

            try:
                article_id = ''
                date = ' '.join(soup.find("span", {'class':"date-posted"}).text.split(' ')[:3])
                category = 'nCov'
                title = soup.find("h1", {'class':"news-title"}).text
                author = soup.find("span", {'class':"editor"}).text
                text = soup.find("div", {'class':"article-content"}).text
            except AttributeError:
                continue
                
            if title in article_list:
                print('Reach latest article')
                break

            print(title, date)
            abscbn_df = abscbn_df.append(pd.Series([article_id,date,category, title,author, text], index = abscbn_df.columns ), ignore_index=True)
            time.sleep(6)
        
        df = df.append(abscbn_df)
        df.to_csv('scraped_data/abscbn_scraped.csv', index = False)
    except:
        df.to_csv('scraped_data/new_abscbn_scraped.csv', index = False)

def get_rappler():
    
    # Listing down all the news articles about COVID
    
    rappler_news = []
    page_link = '/previous-articles?filterMeta=coronavirus%20philippine%20updates'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0)'

    while page_link != False:
        req = Request('https://www.rappler.com' + page_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'})
        content = urlopen(req).read()
        soup = BeautifulSoup(content)

        mydivs = soup.find("div", {'id':"article-finder-result"})

        mydivs = mydivs.find_all("div", {'class':"row"})

        rappler_news += [url.a['href'] for url in mydivs] 
        time.sleep(6)

        try:
            page_link = soup.find("a", {'title':"Next"})['href']
        except:
            page_link = False
        
    rappler_df = pd.DataFrame(columns = ['source_id','date','category','title','author','text'])
    
    
    # Scraping all the articles in the list

    for article in rappler_news:  
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
        req = Request('https://www.rappler.com' + article, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'})
        content = urlopen(req).read()
        soup = BeautifulSoup(content)

        try:
            article_id = ''
            
            date = soup.find("div", {'class':"published"}).text.strip()
            date = re.search("(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?).(\d{2}),.(\d{4})", date)
            date = date[0]
            
            category = 'nCov'
            title = soup.find("h1", {'class':"select-headline"}).text
            author = soup.find("a", {'class':"rappler-headline link"}).text.strip()
            text = soup.find("div", {'class':"cXenseParse"}).text
        except AttributeError:
            continue

        print(title, date)
        rappler_df = rappler_df.append(pd.Series([article_id,date,category, title,author, text], index = rappler_df.columns ), ignore_index=True)
        time.sleep(10)
    
    rappler_df.to_csv('rappler_tracker_scraped.csv', index = False)