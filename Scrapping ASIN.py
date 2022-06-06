#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install latest-user-agents
import numpy as np
from time import sleep
import requests
import os
import pickle
import pandas as pd
from bs4 import BeautifulSoup
from latest_user_agents import get_latest_user_agents, get_random_user_agent


# In[2]:


categories_all_pages=[]
categories = [
    "https://www.amazon.com/s?i=automotive&bbn=15684181&rh=n%3A15684181&dc&fs=true&page=&qid=1649751888&ref=sr_pg_2",
    "https://www.amazon.com/s?i=baby-products&rh=n%3A165796011&fs=true&page=&qid=1649751918&ref=sr_pg_2",
    "https://www.amazon.com/s?i=beauty-intl-ship&rh=n%3A16225006011&fs=true&page=&qid=1649753302&ref=sr_pg_2",
    "https://www.amazon.com/s?i=computers-intl-ship&rh=n%3A16225007011&fs=true&page=&qid=1649753331&ref=sr_pg_2",
    "https://www.amazon.com/s?i=hpc-intl-ship&rh=n%3A16225010011&fs=true&page=&qid=1649755099&ref=sr_pg_2",
    "https://www.amazon.com/s?i=industrial-intl-ship&rh=n%3A16225012011&fs=true&page=&qid=1649755125&ref=sr_pg_2",
    "https://www.amazon.com/s?i=fashion-luggage&bbn=16225017011&page=&qid=1649755153&ref=sr_pg_3",
    "https://www.amazon.com/s?i=pets-intl-ship&rh=n%3A16225013011&fs=true&page=&qid=1649755191&ref=sr_pg_2",
    "https://www.amazon.com/s?i=sporting-intl-ship&rh=n%3A16225014011&fs=true&page=&qid=1649755229&ref=sr_pg_2",
    "https://www.amazon.com/s?i=tools-intl-ship&rh=n%3A256643011&fs=true&page=&qid=1649755249&ref=sr_pg_2",
    "https://www.amazon.com/s?i=toys-and-games-intl-ship&rh=n%3A16225015011&fs=true&page=&qid=1649755270&ref=sr_pg_2",
    "https://www.amazon.com/s?i=arts-crafts&rh=n%3A2617941011&fs=true&page=&qid=1649755294&ref=sr_pg_2",
    "https://www.amazon.com/s?i=electronics&bbn=172282&rh=n%3A172282&dc&fs=true&page=&qid=1649755316&ref=sr_pg_2",
    "https://www.amazon.com/s?k=clothing&i=fashion&rh=n%3A7141123011&dc&page=&qid=1649755340&ref=sr_pg_2",
    "https://www.amazon.com/s?i=digital-music&bbn=163856011&rh=n%3A163856011&dc&fs=true&page=&qid=1649755371&ref=sr_pg_2",
    "https://www.amazon.com/s?i=digital-text&s=relevance&page=&qid=1649755406&ref=sr_pg_2",
    "https://www.amazon.com/s?i=instant-video&page=&qid=1649755431&ref=sr_pg_2",
    "https://www.amazon.com/s?i=movies-tv&bbn=2625373011&rh=n%3A2625373011&dc&fs=true&page=&qid=1649755449&ref=sr_pg_2",
    "https://www.amazon.com/s?i=popular&bbn=5174&rh=n%3A5174&dc&fs=true&page=&qid=1649755483&ref=sr_pg_3",
    "https://www.amazon.com/s?i=software&bbn=229534&rh=n%3A229534&dc&fs=true&page=&qid=1649755523&ref=sr_pg_2"
    ]
for url_main in categories:
    for i in range(2,400):
        url=url_main.split('&page=')
        url=url[0]+'&page='+str(i)+'&ref=sr_pg_'+str(i-1)
        categories_all_pages.append(url)
pd.DataFrame(categories_all_pages).to_csv("All_Pages_links.csv",header=None,index=None)


# In[3]:


def scrap(url):
    while True:
        try:
            agent=get_random_user_agent()
            number=np.random.randint(1,100+1)
            headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }
            proxies={"http": f"http://hjqynrpv-{number}:s2nt3cxp4072@p.webshare.io:80/","https": f"http://hjqynrpv-{number}:s2nt3cxp4072@p.webshare.io:80/"}
            r= requests.get(url,headers=headers,timeout=(2, 6),proxies=proxies)
            code=r.status_code
            if not isinstance(r, type(None)):
                if r.status_code >= 500:
                    print(f"Server Code {code} On hjqynrpv-{number}")
                    if "To discuss automated access to Amazon data please contact" in r.text:
                        print(f"Page {url} was blocked by Amazon on hjqynrpv-{number} Please try using better proxies")
                    elif "To discuss automated access to Amazon" in r.text:
                        print(f"Page {url} was blocked by Amazon on hjqynrpv-{number} Please try using better proxies")
                    else:
                        print(f"Page {url} must have been blocked by Amazon as the status code was {r.status_code}")
                    raise Exception()
                elif r.status_code == 200:
                    print(f"Status Code {code}")
                    r.close()
                    soup=BeautifulSoup(r.content,features='html.parser')
                    if soup != None:
                        return soup
                    else:
                        pass
                else:
                    print(r.status_code)
                    pass
            else:
                pass
                r.close()
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


# In[4]:


def get_asin(categories_all_pages,categories):
    ASIN=[]
    cat=[]
    for index,page in enumerate(categories_all_pages):
        sleep(5)
        soup=scrap(page)
        divs=soup.find('div',{'class':'s-main-slot s-result-list s-search-results sg-row'})
        for div in divs.prettify().split("data-asin"):
            if div[2:12].isupper():
                ASIN.append(div[2:12])
                cat.append(categories[index])
                
        
        if not os.path.exists('ASIN.csv'):
            pd.DataFrame(columns=['ASIN','Category']).to_csv("ASIN.csv",index=None)
        
        l=pd.read_csv("ASIN.csv")
        l1=len(set(l['ASIN'].to_list()))
        l2=len(set(l['ASIN'].to_list()+ASIN))
        while l1==l2:
            sleep(2)
            soup=scrap(page)
            divs=soup.find('div',{'class':'s-main-slot s-result-list s-search-results sg-row'})
            for div in divs.prettify().split("data-asin"):
                if div[2:12].isupper():
                    ASIN.append(div[2:12])
                    cat.append(categories[index])
                    
            l=pd.read_csv("ASIN.csv")
            l1=len(set(l['ASIN'].to_list()))
            l2=len(set(l['ASIN'].to_list()+ASIN))
            print('_',end='')
            
        if os.path.exists('ASIN.csv'):
            df_previous=pd.read_csv("ASIN.csv")
            df_new=pd.DataFrame(ASIN,columns=['ASIN'])
            df_new['Category']=cat
            df_fresh=pd.concat([df_previous,df_new])
            df_fresh.to_csv("ASIN.csv",index=None)
        else:
            pd.DataFrame(columns=['ASIN','Category']).to_csv("ASIN.csv",index=None)
        print(".",end='')      


# In[6]:


if os.path.exists('Batches.csv'):
    with open('Batches.txt', 'rb') as handle:
        batches = pickle.load(handle)
else:
    batches=0
batch_size=20
while True:
    categories=[]
    pages_to_scrap=categories_all_pages[batch_size-20:batch_size+1]
    for i in pages_to_scrap:
        if "&bbn" in i.split('i=')[-1]:
            categories.append(i.split('i=')[-1].split("&bbn")[0])
        else:
            categories.append(i.split('i=')[-1].split("&rh")[0])
    
    get_asin(pages_to_scrap,categories)
    batch_size+=20
    batches+1
    with open('Batches.txt', 'wb') as handle:
        pickle.dump(batches, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('\033[1m','Batch_Complete','\033[0m')
    if len(pages_to_scrap)==0:
        batches=0
        with open('Batches.txt', 'wb') as handle:
            pickle.dump(batches, handle, protocol=pickle.HIGHEST_PROTOCOL)
        break
print("All ASIN Scraped")


# In[ ]:




