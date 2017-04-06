# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 00:17:02 2017

@author: emadezzeldin
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import csv
from bs4 import BeautifulSoup
import requests
import re
import time


def OpenBrowser () : 
    global browser
    current_directory = os.getcwd()
    path_to_chromedriver = current_directory + '/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)

def update_root ():
    global root
    root = lxml.html.fromstring(browser.page_source)
    #print (root)
    
def getEasyApply ():
    return browser.find_elements_by_partial_link_text ('Easy Apply') 

#easyapply1 = getEasyApply(0)
##https://gist.github.com/lrhache/7686903
##def newtab ():
#OpenBrowser ()
#update_root ()
#
#url = 'https://www.linkedin.com/jobs/search/?keywords=python&location=United%20States&locationId=us%3A0&start=' + str(25) 
#browser.get (url)
#
#EasyApply = getEasyApply ()
#easyapply1 = EasyApply [0]
#easyapply1.click()
#
#joburl = str (browser.current_url)
#joburl = 'https://www.linkedin.com/jobs/view/287983696/'
#browser.get (joburl)

# This 1000 loop took 6 hours , This loop finished at page 40. There are about 1000 pages it should have gone to. So it would take 150 hour to reach 1000.
PythonjobsURL = []
Pagenumber = 100
update_root ()
easyapply = getEasyApply () 
while Pagenumber<=1000:
    url = 'https://www.linkedin.com/jobs/search/?keywords=python&location=United%20States&locationId=us%3A0&start=' + str(Pagenumber)
    browser.get(url)
    time.sleep(10)
    easyapply = getEasyApply () 
    print easyapply
    L = len (easyapply)
    for n in range (L):
         time.sleep(5)
         print n
         easyapply = getEasyApply () 
         time.sleep(5)
         easyapply[n].click()
         PythonjobsURL.append(str(browser.current_url))
         update_root ()
         time.sleep(10)
         browser.get(url)
         update_root ()
         time.sleep(5)
    Pagenumber= Pagenumber + 25 
        
    






        
     
