import numpy as np
from time import sleep
import requests
import os
import pickle
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from latest_user_agents import get_latest_user_agents, get_random_user_agent



def Scrap_ALl(url):
    soup,IP,UN=scrap(url)
    print(f"hjqynrpv-{UN} ", IP)
    print(len(soup))
    
    ASIN=url.split('/')[-1]
    date = datetime.now().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    Title=scrap_Title(soup)
    Price=scrap_price(soup)
    Image=scrap_Image(soup)
    Sold_By=scrap_Sold_By(soup)
    Is_New=scrap_Is_New(soup)
    Availability=scrap_Availability(soup)
    Ratting=scrap_Ratting(soup)
    Description=scrap_Description(soup)[:100]
    table=get_tables(soup)
    Brand=scrap_Brand(soup,table)
    Customer_Ratting=scrap_Customer_Ratting(soup,table)
    Seller_Rank=scrap_Seller_Rank(soup,table)
    Date_First_Available=scrap_Data_First_Available(soup,table)
    return url,ASIN,date,time,Title,Price,Image,Sold_By,Is_New,Availability,Ratting,Description,Brand,Customer_Ratting,Seller_Rank,Date_First_Available,table


def scrap_Data_First_Available(soup,table):
#     Date First Available
    if 'Date First Available' in table.keys():
        Date_First_Available=table['Date First Available']
    else:
        try:
            for i in soup.find('div',{'id':'detailBullets_feature_div'}).find_all('li'):
                if "Date First Available" in  i.text.replace('\n','').replace('  ','').strip():
                    Date_First_Available=i.text.replace('\n','').replace('  ','').strip().split(':')[-1].split("\u200e")[-1]
            
            if len(Date_First_Available)==0:
                raise Exception()
        except:
            Date_First_Available=''
    return Date_First_Available


def scrap_Seller_Rank(soup,table):
#     Seller_Rank
    if 'Best Sellers Rank' in table.keys():
        Seller_Rank=table['Best Sellers Rank']
    else:
        try:
            Seller_Rank=soup.find_all("ul", { "class" : "a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"})[-2].text.replace('\n','').replace('  ','').strip().split(':')[-1]
            if len(Seller_Rank)==0:
                raise Exception()
        except:
            Seller_Rank=""
    return Seller_Rank


def scrap_Customer_Ratting(soup,table):
#     Customer_Ratting
    try:
        customer_rating=soup.find("div", { "id" : "averageCustomerReviews_feature_div"}).find_all('a')[-1].text.replace('\n','').strip().strip()
        if len(customer_rating)==0:
            raise Exception()
    except:
        if 'Customer Reviews' in table.keys():
            customer_rating=table['Customer Reviews']
        else:
            customer_rating=''        
    return customer_rating

def scrap_Brand(soup,table):
#     Brand
    if 'Brand' in table.keys():
        brand=table['Brand']
    elif not 'Brand' in table.keys():    
        try:
            brand=soup.find("tr", { "class" : "a-spacing-small po-brand"}).find_all('span')[-1].text.replace('\n','').strip()
            if len(brand)==0:
                    raise Exception()
        except:
            try:
                heading=soup.find("div", { "id" : "productDescription" }).find_all('h3')[-1].text.replace('\n','').replace("  ",'').strip().lower()
                if 'brand' in heading or 'Manufacturer'.lower() in heading :
                    brand=soup.find("div", { "id" : "productDescription" }).find_all('p')[-1].text.replace('\n','').replace("  ",'').strip()
                if len(brand)==0:
                    raise Exception()
            except:
                try:
                    brand=soup.find("a", { "id" : "bylineInfo" }).text.replace('\n','').replace('  ','').strip()
                    if len(brand)==0:
                        raise Exception()
                except:
                    brand=""
    elif 'Manufacturer' in table.keys():
        brand=table['Manufacturer']
    else:
        brand=""
    return brand


def get_tables(soup):
    try:
        ids_table=['productDetails_detailBullets_sections1','productDetails_techSpec_section_1','productDetails_db_sections']
        table={}
        for i in ids_table:
            tb={}
            try:     
                th=soup.find("table", { "id" : i }).find_all('th')
                td=soup.find("table", { "id" : i }).find_all('td')
                for h,d in zip(th,td):
                #     table[h.text.strip()]=d.text.strip().replace('\n','').replace("  ",'').encode('ascii','ignore')
                    table[h.text.strip()]=d.text.strip().replace('\n','').replace("  ",'').split("\u200e")[-1]
                table.update(tb)
            except:
                pass
    except:
        print()
    return table


def scrap_Description(soup):
#     Description
    try:
        desc=soup.find("div", { "id" : "productDescription" }).text.replace('\n','').replace("  ",'').strip()
        if len(desc)==0:
            raise Exception
    except:
        try:
            desc=soup.find("div", { "id" : "feature-bullets" }).text.replace('\n','').replace("  ",'').strip()
            if len(desc)==0:
                raise Exception
        except:
            desc=""
    return desc

def scrap_Ratting(soup):
#     Ratting
    try:
        ratting=soup.find("div", { "id" : "averageCustomerReviews_feature_div"}).find('a').text.replace('\n','').strip()
        if len(ratting)==0:
            raise Exception()
    except:
        ratting=""
    return ratting


def scrap_Availability(soup):
#     Availability
    try:
        Availability=soup.find("div", { "class" : "a-box-group"}).find('div',{'id':'availability'}).text.replace('\n','').strip()
        if len(Availability)==0:
            raise Exception()
    except:
        try:
            Availability=soup.find("div", { "id" : "outOfStock" }).find('div',{'id':"exports_desktop_outOfStock_buybox_message_feature_div"}).find('span').text.replace('\n','').replace('  ','').strip()
            if len(Availability)==0:
                raise Exception()
        except:
            if "in stock".lower() in soup.get_text().lower():
                Availability="In Stock"
            elif "In Stock." in soup.get_text():
                Availability="In Stock"
            elif "Currently unavailable" in soup.get_text():
                Availability="Currently unavailable"
            elif "Temporarily out of stock." in soup.get_text():
                Availability="Temporarily out of stock."
            else:
                Availability='In Stock'
    return Availability


def scrap_Is_New(soup):
#     Is_new
    try:
        if 'new' in soup.select_one("#olp_feature_div a").text.replace('\n','').replace("  ",'').strip().lower():
            is_new="Yes"
        else:
            is_new="No"
    except:
        is_new="No"
#         print("is_new Not Found")    
    return is_new

def scrap_Sold_By(soup):
#     Sold_by
    try:
        sold_by=soup.find("div", { "id" : "exports_desktop_qualifiedBuybox_tabular_feature_div"}).text.replace('\n','').replace("  ",'').strip()
        if len(sold_by)==0:
                raise Exception()
    except:
        try:
            sold_by=soup.find("div", { "class" : "tabular-buybox-container"}).text.replace('\n','').replace("  ",'').strip()
            if len(sold_by)==0:
                    raise Exception()
        except:
            sold_by=""

    return sold_by



def scrap_Image(soup):
#     Image
    try:
        Image=soup.find("div", { "id" : "imgTagWrapperId"}).find('img')['src'].strip()
    except:
        # try:
        #     Image=find("#imgTagWrapperId > img::attr(src)",'CSS')
        #     if len(Image)==0:
        #         raise Exception()
        # except:
        #     try:
        #         Image=find("#landingImage",'CSS')[0].split(" ")
        #         Image=list([i for i in Image if 'src' in i])[0].split('src=')[-1]
        #         if len(Image)==0:
        #             raise Exception()
            # except:
        Image=""

    return Image


def scrap_price(soup):
#     Price:
    try:
        list_price=[]
        list_price.append(soup.select_one(".a-color-secondary .a-size-base span").text.replace('\n','').strip())
        list_price.append(soup.select_one(".apexPriceToPay span").text.replace('\n','').strip())
        if len(list_price)==0:
            raise Exception()
    except:
        try:
            list_price=soup.find("div", { "id" : "corePrice_desktop" }).find('span').text.replace('\n','').replace('  ','').strip()
            if len(list_price)==0:
                raise Exception()
        except:
            try:
                list_price=soup.find('div',{'class':'a-box-group'}).find('span',{'class':'a-offscreen'}).text
                if len(list_price)==0:
                    raise Exception()
            except:
                    list_price=""

    return list_price

def scrap_Title(soup):
#     Title
    try:
        Title=soup.find("div", { "id" : "titleSection"}).text.replace('\n','').strip()
        if len(Title)==0:
            raise Exception()
    except:
        # try:
        #     Title=find("#productTitle::text",'CSS')[0].lstrip()
        #     if len(Title)==0:
        #         raise Exception()
        # except:   
        Title=""

    return Title  



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
            print(f"Status Code {code}")
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
                    # return BeautifulSoup(r.content,features='lxml'),IP,number
                    r.close()
                    return BeautifulSoup(r.content,features='html.parser'),f"hjqynrpv-{number}"

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


def scrap_(url):
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
            # 'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'user-agent': agent,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }
            with requests.get(url, stream=True,headers=headers, proxies={"http": f"http://hjqynrpv-{number}:s2nt3cxp4072@p.webshare.io:80/","https": f"http://hjqynrpv-{number}:s2nt3cxp4072@p.webshare.io:80/"},timeout=(2, 6)) as r:
                IP=r.raw._original_response.fp.raw._sock.getpeername()[0]
                code=r.status_code
                if not isinstance(r, type(None)):
                    if r.status_code >= 500:
                        print("Server Code",code,"On ",IP)
    #                     print("IP ",r.raw._original_response.fp.raw._sock.getpeername()[0],'UN:',number)
                        if "To discuss automated access to Amazon data please contact" in r.text:
                            print(f"Page {url} was blocked by Amazon. Please try using better proxies")
                        elif "To discuss automated access to Amazon" in r.text:
                            print(f"Page {url} was blocked by Amazon. Please try using better proxies")
                        else:
                            print(f"Page {url} must have been blocked by Amazon as the status code was {r.status_code}")
                        raise Exception()
                    elif r.status_code == 200:
                        # return BeautifulSoup(r.content,features='lxml'),IP,number
                        return BeautifulSoup(r.content,features='html.parser'),IP,number

                    else:
                        print(r.status_code)
                        pass
                else:
                    pass
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
