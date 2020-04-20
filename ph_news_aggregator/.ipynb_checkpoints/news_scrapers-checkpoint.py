import urllib
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.request import Request, urlopen
import re


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
            
            print('Next page')

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
                print('Reached latest article')
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
    
    df = pd.read_csv('scraped_data/rappler_tracker_scraped.csv')
    article_list = list(df['title'].unique())

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
            
        if (title in article_list) & (title != 'WATCH: DOH updates on 2019 novel coronavirus') & (title != '#DuterteLive: Updates on enhanced community quarantine'):
            print('Reached latest article ' + title)
            break

        print(title, date)
        rappler_df = rappler_df.append(pd.Series([article_id,date,category, title,author, text], index = rappler_df.columns ), ignore_index=True)
        time.sleep(10)
        
    df = df.append(rappler_df)
    df.to_csv('scraped_data/rappler_tracker_scraped.csv', index = False)
    
    
    
    
def get_mb():
    try:
        mb_ncov_news = []
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0)'


        req = Request('https://news.mb.com.ph/tag/ncov', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive'})


        content = urlopen(req).read()

        #print('reading url')
        soup = BeautifulSoup(content)

        last_page = int(soup.find("ul", {'class':"uk-pagination"}).text[-3:]) + 1  
        
        df_list = pd.read_csv('articles_list/mb_ncov_articles_urls.csv', header = None)
        article_list = df_list[0]
        
        loop = True
        
        print('start')
        for i in range(1, last_page):

            page_link = 'https://news.mb.com.ph/tag/ncov/page' + str(i) + '/'
            print(page_link)
            req = Request(page_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive'})

            content = urlopen(req).read()

            #print('reading url')
            soup = BeautifulSoup(content)

            #print('reading main news section')
            mydivs = soup.find("main", {'class':"tm-content"})

            #print('reading urls in news section')
            mydivs = mydivs.find_all("article", {'class':"uk-article listwiththumb"})
            
            for url in mydivs:
                #print(url.a['href'])
                if url.a['href'] in article_list.values:
                    loop = False
                    print(url.a['href'] + ' stopped latest')
                    break
                else:
                    mb_ncov_news.append(url.a['href'])
            
            if loop == False:
                break
            #mb_ncov_news += [url.a['href'] for url in mydivs]

            #print(i)
            #print(len(mb_ncov_news))
            time.sleep(1)

        to_add = pd.Series(mb_ncov_news)
        #f['articles'] = article_list.append(to_add).reset_index(drop = True)
        #df.to_csv('new_mb_ncov_articles.csv', index = False)
        
        mb_df = pd.DataFrame(columns = ['source_id','date','category','title','author','text'])
        df = pd.read_csv('scraped_data/mb_scraped.csv')
        
        print(len(mb_ncov_news))
        
        for article in mb_ncov_news:  
            user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
            req = Request(article, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive'})
            content = urlopen(req).read()
            soup = BeautifulSoup(content)

            try:
                article_id = ''
                date = soup.find('time').text
                category = 'nCov'
                title = soup.find("h1", {'class':"uk-article-title uk-margin-bottom-remove"}).text
                author = soup.find('strong').text
                art = soup.find_all("p")
                text = ' '.join(item.text for item in art)
            except AttributeError:
                continue

            print(title, date)
            mb_df = mb_df.append(pd.Series([article_id,date,category, title,author, text], index = mb_df.columns ), ignore_index=True)
            time.sleep(3)

        df = df.append(mb_df)
        df.to_csv('scraped_data/mb_scraped.csv', index = False)
        
        df_list[0].append(to_add).reset_index(drop = True).to_csv('articles_list/mb_ncov_articles_urls.csv', index = False)
        
    except: 
        print('Error')
        
def get_mt():    
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0)'
    page_url = 'https://www.manilatimes.net/?s=coronavirus'
    manila_times_news = []

    df_list = pd.read_csv('articles_list/m_times_articles_urls.csv', header = None);
    article_list = df_list[0]

    while page_url != False:
        req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'})
        content = urlopen(req).read()
        soup = BeautifulSoup(content)
        res = (soup.find_all('a',{'rel':"bookmark"}))

        #manila_times_news += [url['href'] for url in res]
        for url in res:
            if url['href'] in article_list.values:
                page_url = False
                print(url['href'] + ' stopped latest')
                break
            else:
                manila_times_news.append(url['href'])

        if page_url == False:
            break

        date = (soup.find_all('time'))

        page_link = soup.find('div',{'class':"page-nav"} )

        time.sleep(3)
        if date[0]['datetime'] < '2020-01-20':
            page_url = False
        else:
            page_url =  page_link.find_all('a')[-1]['href']
            print(page_url)

    mt_df = pd.DataFrame(columns = ['source_id','date','category','title','author','text'])
    df = pd.read_csv('scraped_data/manila_times_scraped.csv')

    try:    
        for article in manila_times_news:  
            user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
            req = Request(article, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'})
            content = urlopen(req).read()
            soup = BeautifulSoup(content)

            try:
                article_id = ''

                date = soup.find('time').text

                category = 'nCov'
                title = soup.find('h1', {'class' : 'tdb-title-text'}).text
                author = soup.find('a', {'class' : 'tdb-author-name'}).text

                text = soup.find('div', {'class' : 'td-post-content'})
                text.find_all('p')

                paragraph = ""
                for x in text.find_all('p'):
                    paragraph += x.text.strip() + " " 

                text = paragraph
            except AttributeError:
                continue

            if (title in df['title'].values):
                print('Reached latest article')
                break

            print(title, date)
            mt_df = mt_df.append(pd.Series([article_id,date,category, title,author, text], index = mt_df.columns ), ignore_index=True)
            time.sleep(2)

        df = df.append(mt_df)
        df.to_csv('scraped_data/manila_times_scraped.csv', index = False)

        df_list[0].append(manila_times_news).reset_index(drop = True).to_csv('articles_list/m_times_articles_urls.csv', index = False)

    except:
        df = df.append(mt_df)
        df.to_csv('scraped_data/manila_times_scraped.csv', index = False)

