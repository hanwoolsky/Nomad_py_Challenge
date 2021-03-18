import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

job_result = requests.get(alba_url)
indeed_soup = BeautifulSoup(job_result.text, "html.parser")

table = indeed_soup.find("div", {"id": "MainSuperBrand"}).find("ul", {"class": "goodsBox"})

superbrand = table.find_all("a", {"class": "goodsBox-info"})
brand_size = len(superbrand)

brand_name = []
job_url = []
for i in range(brand_size):
  brand_name.append(superbrand[i].find("span", {"class": "company"}).string)
  job_url.append(superbrand[i].get('href'))

def page(link):
  page_result = requests.get(link)
  page_soup = BeautifulSoup(page_result.text, "html.parser")
  page_list = page_soup.find("div", {"id": "NormalInfo"})
  count = page_list.find("p", {"class": "jobCount"})
  page = int(count.text.replace('건','').replace(',',''))
  return page

place = []
title = []
Time = []
pay = []
Date = []

def make_csv(link, page):
  csv_result = requests.get(link+f"job/brand/?pagesize={page}")
  csv_soup = BeautifulSoup(csv_result.text, "html.parser")
  csv_list = csv_soup.find("div", {"id": "NormalInfo"})
  for i in range(page):
    place.append(csv_list.find_all("td", {"class": "local first"})[i].text.split("\xa0")[0] + " " + csv_list.find_all("td", {"class": "local first"})[i].text.split("\xa0")[1])
    title.append(csv_list.find_all("td", {"class": "title"})[i].text)
    Time.append(csv_list.find_all("td", {"class": "data"})[i].text) 
    pay.append(csv_list.find_all("td", {"class": "pay"})[i].text) 
    Date.append(csv_list.find_all("td", {"class": "regDate last"})[i].text)
    list_dictionary = {
      'place': place[i],
      'title': title[i],
      'time': Time[i],
      'pay': pay[i],
      'date': Date[i]
    }
    jobs.append(list_dictionary)
  return jobs

def save_to_file(brand_name, jobs):
  file = open(f"{brand_name}.csv", mode = "w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for i in range(len(jobs)-1):
    writer.writerow(list(jobs[i].values()))
  return
 
jobs = []
for i in range(brand_size - 1):
  #print(brand_name[i])
  jobs.append(make_csv(job_url[i], page(job_url[i])))
  save_to_file(brand_name[i], jobs)
  jobs = []
