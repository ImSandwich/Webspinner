import os
import sys
import csv
import time
import mmap
import queue
import shutil
import urllib
import datetime
import lxml.html
import threading
from os import listdir
from bs4 import BeautifulSoup
from os.path import isfile, join
from urllib.request import urlopen, Request

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def main():
  source_words = ["cryptography"]
  
  for word in source_words:
    definitions_of(word)

def definitions_of(word):
  word = word.replace(" ", "+").replace("'", "")
  print(word)
  link = 'https://www.google.com/search?q=define+"' + word + '"'
  req = Request(link, headers = headers)
  page = urlopen(req)
  soup = BeautifulSoup(page.read(), 'lxml')

  file = open("error.html", "w")
  # print(soup.prettify(), file = file)
  # file.close()

  results = []
  # Normal Definition 
  if(soup.find("div", {'class':'lr_container'}) != None):
    all_defs = soup.find("div", {'class':'lr_container'}).find_all('li')
    # print(all_defs.prettify(), file = file)
    # file.close()
    for definition in all_defs:
      if(definition.find('div', {'style':'display:inline'}) != None):
        results.append(definition.find('div', {'style':'display:inline'}).get_text().lstrip().rstrip())

  # Web definition
  if(soup.find("div", {'class':'xpdopen'}) != None):
    definition = soup.find("div", {'class':'xpdopen'})
    if(definition.find('span', {'class':'e24Kjd'}) != None):
      results.append(definition.find('span', {'class':'e24Kjd'}).get_text().lstrip().rstrip())

  print(results)
  return results

if __name__ == '__main__':
  main()