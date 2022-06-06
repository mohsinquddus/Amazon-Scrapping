#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from time import sleep
import requests
import os
import pickle
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from functions import *
from latest_user_agents import get_latest_user_agents, get_random_user_agent
from platform import python_version
python_version()


# In[2]:


df_ASIN=pd.read_csv("ASIN.csv")
df_ASIN=df_ASIN.drop_duplicates().reset_index()
ASINS=df_ASIN['ASIN'].to_list()
category=df_ASIN['Category'].to_list()
products_links=["https://www.amazon.com/dp/"+i for i in ASINS]
# print(len(products_links))
# print(len(category))


# In[3]:


# products_links[0:5]


# In[39]:


def scrap_batch(links,Categories):
    product_detail={'Market':[],'Category':[],'URL':[],"ASIN":[],"Date":[],"Time":[],
                   "Title":[],"Ratting":[],"Availability":[],"Desc":[],
                    "list_price":[],"Image":[],"Brand":[],"Seller_Rank":[],
                    "customer_ratting":[],"ship_by":[],"sold_by":[],"Is_new":[],
                    "Date_First_Available":[],"Tables":[]}

    if not os.path.exists('Products_Detail.csv'):
        new=pd.DataFrame(product_detail)
        new.to_csv('Products_Detail.csv',index=False)

    for idx,i in enumerate(links):
        category=Categories[idx]
        dff=pd.read_csv('Products_Detail.csv')
        url=i
        ASIN=url.split('/')[-1]
        if '.com' in url:
            market="US"
        else:
            market="Not US"
            
        if dff[dff['ASIN'].isin([str(ASIN)])].shape[0]==0:
            time.sleep(3)
            try:
                for j in range(15):
                    soup,UN=scrap(i)
                    table=get_tables(soup)
                    if len(soup)==7 and len(table)!=0:
                        break
                if len(soup)!=7:
                    raise Exception()
            except:
                while True:
                    soup,UN=scrap(i)
                    if len(soup)==7:
                        break
                    
            print(UN,end=' ')
            print(len(soup))
            date = datetime.now().strftime("%d/%m/%Y")
            Time = datetime.now().strftime("%H:%M:%S")
            Title=scrap_Title(soup)
            Price=scrap_price(soup)
            Image=scrap_Image(soup)
            Sold_By=scrap_Sold_By(soup)
            Ship_By=Sold_By.split('Sold by')[0]
            Sold_By=Sold_By.split('Sold by')[-1]
            Is_New=scrap_Is_New(soup)
            Availability=scrap_Availability(soup)
            Ratting=scrap_Ratting(soup)
            table=get_tables(soup)
            Description=scrap_Description(soup)
            Brand=scrap_Brand(soup,table)
            Customer_Ratting=scrap_Customer_Ratting(soup,table)
            Seller_Rank=scrap_Seller_Rank(soup,table)
            Date_First_Available=scrap_Data_First_Available(soup,table)
            if len(Title)==0:
                Availability=""
                Is_New=""
#                 table=""
            else:
                product_detail['Market'].append(market)
                product_detail['Category'].append(category)
                product_detail['URL'].append(url)
                product_detail['ASIN'].append(ASIN)
                product_detail['Date'].append(date)
                product_detail['Time'].append(Time)
                product_detail['Title'].append(Title)
                product_detail['Ratting'].append(Ratting)
                product_detail['Availability'].append(Availability)
                product_detail['Desc'].append(Description)
                product_detail['list_price'].append(Price)
                product_detail['Image'].append(Image)
                product_detail['Brand'].append(Brand)
                product_detail['Seller_Rank'].append(Seller_Rank)
                product_detail['customer_ratting'].append(Customer_Ratting)
                product_detail['sold_by'].append(Sold_By)
                product_detail['ship_by'].append(Ship_By)
                product_detail['Is_new'].append(Is_New)
                product_detail['Date_First_Available'].append(Date_First_Available)
                product_detail['Tables'].append(table)

    if os.path.exists('Products_Detail.csv'):
        old=pd.read_csv('Products_Detail.csv')
        old
        new=pd.DataFrame(product_detail)
        df=pd.concat([old,new])
        df.to_csv('Products_Detail.csv',index=False)
    else:
        new=pd.DataFrame(product_detail)
        new.to_csv('Products_Detail.csv',index=False)


# In[40]:


if os.path.exists('Batches_products.txt'):
    with open('Batches_products.txt', 'rb') as handle:
        batches = pickle.load(handle)
else:
    batches=0
batch_size=20
while True:
    ASINs=products_links[batch_size-20:batch_size+1]
    Categories=category[batch_size-20:batch_size+1]
    scrap_batch(ASINs,Categories)
    batch_size+=20
    batches+=1
    with open('Batches_products.txt', 'wb') as handle:
        pickle.dump(batches, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('\033[1m','Batch_Complete','\033[0m')
    if len(ASINs)==0:
        batches=0
        with open('Batches_products.txt', 'wb') as handle:
            pickle.dump(batches, handle, protocol=pickle.HIGHEST_PROTOCOL)
        break
    
print("All Products Scraped")

