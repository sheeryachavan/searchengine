### WEB CRAWLER FOR FOODFOOD.COM ###

import requests
import bs4
import re

from pymongo import MongoClient
import dns
from config import MongoConnection

category = ["course", "cuisine", "occasion", "show"]

client = MongoConnection()
db = client.foodfood

for i in range(len(category)):
    r = requests.get("https://www.foodfood.com/recipes/" + category[i])
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    
    cat = []       # List of Categories Within Major Categories
    for heading in soup.find_all("div", {"class": "col-md-6"}):
        for link in heading.find_all("a"):
            link = link.get("href")
            if re.search("categories", link):
                link = link.split('/')[2]
                cat.append(link)
                
    
    for i in range(len(cat)):
        page_count=1
        while page_count < 10:
            url = "https://www.foodfood.com/categoriesLoad/" + cat[i] + "?page=" + str(page_count)
            main_req = requests.get(url)
            main_soup = bs4.BeautifulSoup(main_req.text, "html.parser")
            
            link_list = []
            for link in main_soup.find_all("div", {"class": "recipe-box typ-recp-box"}):
                for link in link.find_all('a'):
                    rec_link = link.get('href')
                    rec_req = requests.get(rec_link)
                    rec_soup = bs4.BeautifulSoup(rec_req.text, 'html.parser')
                    link_list.append(rec_link)
                    
                    rec_dict = {}
                    for rec_det in rec_soup.find_all('div', {"class": "container"}):

                        try:
                            image = rec_det.find('div', {"claas": "custom-gallery"})

                            rec_dict["image"] = image.img['src']
                            
                            title = rec_det.find("h1", {"class": "non-veg"})
                            title = title.text.strip()                      # Title of the recipe
                            rec_dict["title"]= title

                            recipe_info = rec_det.find_all('div', {"class": "text"})
                            for rec in range(0,2):
                                time_info,time = recipe_info[rec].p.text.strip().split(':')
                                rec_dict[time_info] = time
                                
                            print()

                            key_ing = rec_det.find('div', {"class": "key-ingredients"})
                            if key_ing.find_all('h4'):
                                print()
                                rec_dict["key_ing"] = [i.strip() for i in key_ing.text.strip().split(":")[1].split('\n') if i]
                                
                            short_des = rec_det.find('div', {"class": "recip-short-discription"})
                            rec_dict["desc"] = short_des.p.text.replace('\n',' ')
                        
                            rec_dict["link"] = rec_link
                            result=db.reviews.insert_one(rec_dict)
                        except:
                            pass
            page_count += 1