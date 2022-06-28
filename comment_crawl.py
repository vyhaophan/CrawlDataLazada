#get link

from bs4 import BeautifulSoup
import sys
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import pandas as pd
import numpy as np

#crawl links of products on the lazada
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
base_url = 'https://www.lazada.vn/vong-tay-thoi-trang-nu-2/?rating=1'
driver = webdriver.Firefox(executable_path='D:\\geckodriver.exe')
driver.get(base_url)
#time.sleep(5)
#page = requests.get(base_url,headers=headers)
time.sleep(5)
soup = BeautifulSoup(driver.page_source,"html.parser")
#soup = BeautifulSoup(driver.page_source,"html.parser")
script = soup.find_all("script",{"type": "application/ld+json"})
script = str(script[1])
script = script.replace("</script>","").replace("<script type=\"application/ld+json\">","")
productlinks = []
for element in json.loads(script)["itemListElement"]:
        if "url" in element:
                productlinks.append(element["url"])
#them giao thuc http
for i in range(len(productlinks)):
        productlinks[i] = "https:" + productlinks[i]
print(productlinks)

#crawl reviews and title
titles = []

reviews =[]

description = []

rating = []

prices = []
for link in productlinks:
        #sub_page = requests.get(link,headers=headers)
        #sub_soup = BeautifulSoup(sub_page.text,"lxml")
        driver.get(link)
        time.sleep(5)
        sub_soup = BeautifulSoup(driver.page_source,"html.parser")
        #print(soup)
        #find titles
        title = sub_soup.find("h1",{"class":"pdp-mod-product-badge-title"}).get_text()
        print(title)
        #find reviews
        script = sub_soup.find_all("script", {"type": "application/ld+json"})
        script = str(script[0])
        script = script.replace("</script>","").replace("<script type=\"application/ld+json\">","")
        #print(script)
        

        for element in json.loads(script)["review"]:
            if "reviewBody" in element:
                reviews.append(element["reviewBody"])
                title = driver.find_element_by_class_name('pdp-mod-product-badge-title').text
                titles.append(title)
                if "reviewRating" in element:
                        rate = element["reviewRating"]["ratingValue"]
                        rating.append(rate)
                if "reviewRating" not in element:
                        rating.append(np.nan)
                if "description" in json.loads(script)  :        
                        des = json.loads(script)["description"]
                        description.append(des)
                if "description" not in json.loads(script):
                        description.append(np.nan)
                if "offers" in json.loads(script):
                        price = json.loads(script)["offers"]["lowPrice"]
                        prices.append(price)
        # reviews.append([review_loop])
        # #find avg rating
        # if "aggregateRating" in json.loads(script):
        #         rate = json.loads(script)["aggregateRating"]["ratingValue"]
        #         rates.append(rate)
        # if"aggregateRating" not in json.loads(script):
        #         rates.append(np.nan)
        # #find price of product
        # if "offers" in json.loads(script):
        #         price = json.loads(script)["offers"]["highPrice"]
        #         prices.append(price)
        # if "offers" not in json.loads(script):
        #         prices.append(np.nan)

print(titles)
print(reviews)
print(rating)
print(description)

data_la = pd.DataFrame()
data_la['rating'] = rating
data_la['description'] = description
data_la['review'] = reviews
data_la['titles'] = titles
data_la['price'] = prices

data_la.to_csv('lazada_comment4.csv')

