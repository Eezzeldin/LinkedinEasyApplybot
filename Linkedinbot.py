import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import time
import sqlite3

def openbrowser():
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

def getEasyApply_links():
    return [str(element.get_attribute("href")).split('?') [0] for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title") and 'Easy Apply' in element.text.split("\n")]

def getEasyApply_text():
    def toString(a):
        ilist = []
        for i in a:
            jlist = []
            for j in i:
                try:
                    jlist.append (str(j))
                except:
                    jlist.append ('NA')
                    continue
            ilist.append (jlist)
        return ilist
    return toString ([element.text.split("\n") for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title") and 'Easy Apply' in element.text.split("\n")])

def scroll (num):
    url = 'https://www.linkedin.com/jobs/search/?keywords=python&location=United%20States&locationId=us%3A0&start=' + str(num)
    browser.get (url)

#
#a: unicode text    b:link
def mylist (a,b):
    mylist = []
    #jobtitles = []
    for i in range(len(b)):
        jobtitle = a[i] [1]
        company  = a[i] [3]
        location = a[i] [5]
        description = a[i] [6]
        time     = a[i] [-2]
        joblink  = b[i]
        mylist.append ([joblink ,jobtitle,company,location,description,time])
    return mylist

PythonJobs = []
def Go ():
    global PythonJobs
    counter = 1
    for Pagenumber in range (25,1000,25) :
          counter = counter + 1
          print str (counter)
          #time.sleep (5)
          #browser.execute_script("time.sleep(1) ;window.scrollTo(0, document.body.scrollHeight);")
          elem = browser.find_element_by_tag_name('a')
          for i in range (500):
              elem.send_keys (Keys.ARROW_DOWN)          
          #time.sleep(1)
          a = getEasyApply_text()    
          b = getEasyApply_links()
          #time.sleep (5)
          PythonJobs += mylist (a,b)
          #PythonJobs += b
          #time.sleep (1)
          scroll (Pagenumber)    
          #print mylist(a,b)
          print "==============" + str(len(b)) +"=============================="
          time.sleep (5)

#input [joblink , job title]
def store ():
    conn = sqlite3.connect ("linkedin.sqlite")
    cur  = conn.cursor()
    cur.executescript ('''  DROP TABLE IF EXISTS linkedin ''')
    cur.execute ('''  CREATE TABLE IF NOT EXISTS linkedin (Joblink VARCHAR , Jobtitle VARCHAR , Company VARCHAR ,Location VARCHAR , Description VARCHAR , Time VARCHAR ) ''')
    #PythonJobs = ['https://www.linkedin.com/jobs/view/289092819/',
    #  'Senior Python Developer, Enterprise Products & Services']
    for joblist in PythonJobs:
         jobtimepost= joblist[5]
         jobdescript= joblist[4]
         joblocation= joblist[3]
         jobcompany = joblist[2]
         myjobtitle = joblist[1]
         myjoblink  = joblist[0]
         cur.execute (''' INSERT INTO linkedin (Joblink , Jobtitle,Company,Location,Description,Time) VALUES (?,?,?,?,?,?)''' , (myjoblink,myjobtitle,jobcompany,joblocation,jobdescript,jobtimepost))
    #myjoblink  = 'Emad'
    #myjobtitle = 'Senior Python Developer, Enterprise Products & Services'
    conn.commit()
    cur.close()
