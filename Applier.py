'''
Introduction:
=============
The applier job is to apply for jobs already scraped by the scraper.py and stored in a sqllite database.
# Assume you have read the data and this is the link of interest
#https://www.linkedin.com/jobs/view/285570962/

Operation scheme
================
To use the applier follow these steps
1 - invoke the openbrowser function
2 - login to your linkedin account
3 - invoke the run function 

#Code Opeartion
===============
#open brower
#put link
#detect easy apply
#press
#upload resume
#detect and press submit
#move on to the next link

'''


import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import time
import sqlite3
import random

conn = sqlite3.connect ('linkedin.sqlite')
cur  = conn.cursor()
urls = cur.execute('''SELECT DISTINCT * FROM Python3 ''')
myurls = [str (url[0]) for url in urls]
cur.close()


def openbrowser():
    global browser
    current_directory = os.getcwd()
    path_to_chromedriver = current_directory + '/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)

#detect any button
def getButton(tag,ButtonName):
    ElementsList = browser.find_elements_by_tag_name (tag)
    for x in ElementsList:
            if str(x.text) == ButtonName:
                print ('Found Button')
                return x
def checkbutton (tag,ButtonName):
    ElementsList = browser.find_elements_by_tag_name (tag)
    TextElements = []
    for x in ElementsList:
        TextElements.append(x.text)
    return ButtonName in TextElements

#click easy apply button
def easyapply ()  : 
    print ('Entered Easy Apply')
    time.sleep (random.randint (2,8))
    easyapply = getButton('span','Easy Apply')
    time.sleep (random.randint (2,8))
    easyapply.click()
    print ('I clicked the button')

def add_resume():
    #time.sleep (random.randint (0.5,1))
    browser.find_element_by_id('file-browse-input').send_keys(os.getcwd()+"/Technical Resume.docx")

# submit your application
def submitapplication():
    submit = getButton('button','Submit application')
    submit.click()
    
def unfollow ():
    followcheckbox = browser.find_element_by_id ('follow-company')
    followcheckbox.click()   
    
def sidesubmit():
    submit = getButton('button','Submit')
    submit.click()    

def Apply ():
    print ('Entered apply')
    easyapply () #pressbutton
    print ('Pressed Easy Apply')
    add_resume() #upload resume
    time.sleep (random.randint (1,8))
    unfollow ()
    submitapplication() #submit
    time.sleep (1)

def run ():
    jobcounter = 0
    misscounter = 0 
    for url in myurls[100:]:
        try:
            print ('I am inside try')
            browser.get (url)
            Apply ()
            jobcounter = jobcounter + 1
            time.sleep (random.randint (2,5))
            print ('Applied:%s' %url , 'JobCounts:%s' %jobcounter )
        except:
            time.sleep (random.randint (2,5))
            misscounter = misscounter + 1
            print ('Not Applied' , 'MissCounts:%s' %misscounter)
            if checkbutton ('button','Submit'):sidesubmit()
            continue
        
