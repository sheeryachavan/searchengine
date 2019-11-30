#!/usr/bin/env python
# coding: utf-8

# In[17]:


import os
import queue
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.parse import urldefrag
import urllib.robotparser
from selenium import webdriver
from reppy.robots import Robots
import requests
requests.adapters.DEFAULT_RETRIES = 1
from textblob import TextBlob
from textblob import Word


# In[18]:


def is_absolute(url):
    """Determine whether URL is absolute."""
    return bool(urlparse(url).netloc)


# In[19]:


with open("../static/drop_ing.txt") as f:
    drop_words = f.readlines()
drop_words = [x.strip() for x in drop_words]


# In[25]:


def filter_ing(ing):
    global drop_words
    for word in drop_words:
        if word in ing:
            ing = re.sub((r"\b%s\b"%word),"",ing)
    ing = re.sub('[^a-zA-Z0-9 \n\.]', '', ing)
    text_blob_object = TextBlob(ing)
    document_words = text_blob_object.noun_phrases.singularize()
    print(document_words)
    return ing.strip()


# In[26]:


def scrap_link(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')

    rec_det = {}        # Storing all recipe details inside this list
    rec_det["link"] = link
    for title in soup.find_all("h3"):
        #print(title)
        rec_det["title"] = title.text

    for image in soup.find_all("figure", {"class": "article-image"}):
        #print(image.meta["content"])
        rec_det["image"] = image.meta["content"]

    for i in soup.find_all('li', {'class': 'prep-time'}):
        #print(i.text)
        rec_det["Prep"] = i.text.split(":")[1].strip()
    for i in soup.find_all('li', {'class': 'cook-time'}):
        #print(i.text)
        rec_det["Cook"] = i.text.split(":")[1].strip()
    rec_det["Ingredients"] = []
    for ing in soup.find_all('span', {'class': 'ingredient-label'}):
    #     print(ing.text)     # All Ingredients
        rec_det["Ingredients"].append(filter_ing(ing.text.strip()))
    allp = []
    for desc in soup.find_all('p'):
        #print(method.text)
        allp.append(desc.text)
    rec_det["desc"] = allp[1].split(".")[0]
    print(rec_det)


# In[27]:


def saveContentInHeirarchy(content,url):
    l_objPath = urlparse(url).netloc + urlparse(url).path
    if os.path.exists(l_objPath):
        print("chillax")
    else:
        try:
            os.makedirs(l_objPath)
        except OSError:
            print ("This directory cant be created")
#         print ("creating new path")
    try:
        filepath = l_objPath+"/"+re.sub('[^0-9a-zA-Z]+','-',l_objPath)+".txt"
        with open(filepath,"w",encoding = "utf-8") as newFile:
            newFile.write(content)
    except OSError:
        print ("This directory cant be created")


# In[28]:


options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome("C:\\Users\\shree\\Downloads\\Softwares\\chromedriver_win32\\chromedriver.exe",options=options)
q = queue.Queue()
urlsAlreadyVisited = set()
seed = "https://www.foodrepublic.com/recipes"
q.put(seed)
print(urldefrag(seed)[0])
urlsAlreadyVisited.add(urldefrag(seed)[0])
robots = Robots.fetch('http://www.foodrepublic.com/robots.txt')
agent = robots.agent('User-agent')


# In[1]:


while True:
    url = q.get()
    driver.get(url)    
    soup = BeautifulSoup(driver.page_source,'html.parser')    
#     saveContentInHeirarchy(str(soup.extract()),url)
    links = soup.find_all('a')
    for link in links:
        u = link.get('href')
        if not is_absolute(u):
            u =  urljoin(url,u)
        if "foodrepublic.com/recipes" in u and "@foodrepublic.com" not in u:
            url_string = urldefrag(u)[0]
            if url_string not in urlsAlreadyVisited:
                if agent.allowed(u):
                    q.put(u)
                    scrap_link(u)
                    urlsAlreadyVisited.add(u)
    if q.empty():
        break
    print("Queue size:{}".format(q.qsize()))
    time.sleep(0.05)


# In[ ]:


with open("urlsVisited.txt","w+", encoding='utf-8') as urlsVisited:
        for url in urlsAlreadyVisited:
            urlsVisited.write(url+"\n")


# In[ ]:




