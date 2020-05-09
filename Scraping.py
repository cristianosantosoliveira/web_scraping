from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as soup
import re
from collections import namedtuple
import pandas as pd
import csv
import os

d = webdriver.Chrome('C:/Desenvolvimento/Python/Web Scraping/chromedriver')
d.get('https://www.timeshighereducation.com/world-university-rankings/2018/world-ranking#!/page/0/length/25/sort_by/rank/sort_order/asc/cols/scores')
def page_results(html):
   school = namedtuple('school', ['ranking', 'name', 'location', 'scores'])
   rankings = [i.text for i in soup(html, 'lxml').find_all('td', {'class':'rank sorting_1 sorting_2'})]
   names = [i.text for i in soup(html, 'lxml').find_all('a', {'class':'ranking-institution-title'})]
   locations = [i.text for i in soup(html, 'lxml').find_all('div', {'class':'location'})]
   full_scores = [i.text for i in soup(html, 'lxml').find_all('td', {'class':re.compile('scores\s+[\w_]+\-score')})]
   final_scores = [dict(zip(['overall', 'teaching', 'research', 'citations', 'income', 'outlook'], full_scores[i:i+6])) for i in range(0, len(full_scores), 6)]
   return [school(*i) for i in zip(rankings, names, locations, final_scores)]

Select(d.find_element_by_xpath("//select[@name='datatable-1_length']")).select_by_value('-1')

pages = [page_results(d.page_source)]
links = d.find_elements_by_tag_name('a')
for link in links:
   if link.text.isdigit():
      try:
        link.click()
        pages.append(page_results(d.page_source))
      except:
        pass
d.close()

unpack, *restsoup  = pages

with open('World University.csv', 'w', newline='' ) as file:
  wrtitefile = csv.writer(
      file,
      delimiter=','
      #quotechar='',
      #quoting=csv.QUOTE_ALL
  )
  wrtitefile.writerow(['Ranking',  'Name', 'Location', 'Overall', 'Teaching', 'Research', 'Citations', 'Income', 'Outlook'])

  for data in unpack:
    wrtitefile.writerow(
              [
                data[0].replace("=",""),
                data[1].replace("'", "'''").encode("utf-8"),
                data[2],
                data[3]['overall'],
                data[3]['teaching'],
                data[3]['research'],
                data[3]['citations'],
                data[3]['income'],
                data[3]['outlook']
              ]
          )