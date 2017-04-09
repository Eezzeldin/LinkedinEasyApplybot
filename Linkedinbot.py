import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import csv
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

PythonJobs = []
def run ():
    for Pagenumber in range (25,975,25) :
          scroll (Pagenumber)
          print "================================================================="
          time.sleep (15)
          Easy = getEasyApply ()
          L    = len (Easy)
          print 'Length of Easy apply' + len (Easy)
          for j in range (L):
              EasyApply= getEasyApply ()
              time.sleep (10)
              print EasyApply
              try:
                  print "Now working on element no." , j
                  EasyApply[j].click()
                  time.sleep (5)
                  PythonJobs.append([str(browser.current_url),str (browser.find_element_by_tag_name ('h1').text) , Pagenumber,j])
              except:
                  continue
              print ' finished working on element number' + str (j)
              scroll (Pagenumber)


#element.get_attribute("href")
#[str(element.get_attribute("href")) for element in browser.find_elements_by_partial_link_text ('Easy Apply')]
#Links#[str(element.get_attribute("href")).split('?') [0]  for element in browser.find_elements_by_partial_link_text ('Easy Apply') ]
#Texts#[str(element.text) for element in browser.find_elements_by_partial_link_text ('Easy Apply')]
#[str(element.text) for element in browser.find_elements_by_partial_link_text ('Easy Apply') if str (element.text).startswith ("Job Title")]
#[element.text for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title")]
#[element.text.split("\n") for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title") and 'Easy Apply' in element.text.split("\n")]


#[element.text.split("\n") for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title") and 'Easy Apply' in element.text.split("\n")]
#


#x =[element.text.split("\n") for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title") and 'Easy Apply' in element.text.split("\n")]
#y = [str(element.get_attribute("href")).split('?') [0] for element in browser.find_elements_by_tag_name ('a') if element.text.startswith("Job Title") and 'Easy Apply' in element.text.split("\n")]
#



#a: unicode text    b:link
def mylist (a,b):
    mylist = []
    #jobtitles = []
    for i in range(len(b)):
        jobtitle = a[i] [1]
        joblink  = b[i]
        mylist.append ([joblink ,jobtitle])
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
#https://www.linkedin.com/jobs/view/263609380/
#https://www.linkedin.com/jobs/view/279050467/

# sql lite cursor , file handle
#cur points at the database
#Establish connection
#input [joblink , job title]
def store ():
    conn = sqlite3.connect ("linkedin.sqlite")
    cur  = conn.cursor()
    cur.executescript ('''  DROP TABLE IF EXISTS linkedin ''')
    cur.execute ('''  CREATE TABLE IF NOT EXISTS linkedin (Joblink VARCHAR , Jobtitle VARCHAR) ''')
    #PythonJobs = ['https://www.linkedin.com/jobs/view/289092819/',
    #  'Senior Python Developer, Enterprise Products & Services']
    for joblist in PythonJobs:
         myjobtitle = joblist[1]
         myjoblink  = joblist[0]
         cur.execute (''' INSERT INTO linkedin (Joblink , Jobtitle) VALUES (?,?)''' , (myjoblink,myjobtitle))
    #myjoblink  = 'Emad'
    #myjobtitle = 'Senior Python Developer, Enterprise Products & Services'
    conn.commit()
    cur.close()
