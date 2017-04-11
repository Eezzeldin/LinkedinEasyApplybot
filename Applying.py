# Assume you have read the data and this is the link of interest
#https://www.linkedin.com/jobs/view/285570962/

#open brower
#put link
#detect easy apply
#press
#upload resume
#detect and press submit
#move on to the next link

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
import time
import sqlite3

conn = sqlite3.connect ('linkedin.sqlite')
cur  = conn.cursor()
urls = cur.execute(''' SELECT Joblink FROM linkedin  ''')
myurls = [str (url[0]) for url in urls]
cur.close()


#open browser
def openbrowser():
    global browser
    current_directory = os.getcwd()
    path_to_chromedriver = current_directory + '/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
def update_root ():
    global root
    root = lxml.html.fromstring(browser.page_source)
    #print (root)

#detect any button
def getButton(tag,ButtonName):
    update_root ()
    ElementsList = browser.find_elements_by_tag_name (tag)
    for x in ElementsList:
            if str(x.text) == ButtonName:
                print 'Found Button'
                return x
def checkbutton (tag,ButtonName):
    update_root ()
    ElementsList = browser.find_elements_by_tag_name (tag)
    TextElements = []
    for x in ElementsList:
        TextElements.append(x.text)
    return ButtonName in TextElements

#click easy apply button
def easyapply ()  :
    #actually applying
    #easyapply = browser.find_elements_by_class_name ('a11y-text') [-1]
    update_root ()
    #ElementsList = browser.find_elements_by_tag_name ('span')
    easyapply = getButton('span','Easy Apply')
    easyapply.click()
    update_root ()
    

#Add the resume from the path its saved int
def add_resume():
    browser.find_element_by_id('file-browse-input').send_keys(os.getcwd()+"/Technical Resume.docx")

# submit your application
def submitapplication():
    #ElementsList = browser.find_elements_by_tag_name ('button')
    submit = getButton('button','Submit application')
    submit.click()
    update_root ()

#extracting links from database
# connect to database
#conn = sqlite3.connect ('linkedin.db')
#cur  = conn.cursor()
# connect to TABLE
#urlinks = [cur.execute('''SELECT VALUES Links FROM TABLE linkedin ''')]
# extract links from TABLE
# save links in a list

def Apply ():
    #pressbutton
    easyapply ()
    #upload resume
    add_resume()
    #submit
    submitapplication()
    #pass

#T1 : Easy App    T2:No Easy App

def run ():
    #scrolling through url list
    #open link in browser
    #put link
    for url in myurls:
    #url = 'https://www.linkedin.com/jobs/view/272687969/'
        browser.get (url)
    #check for button easy apply   ****
        #checkbutton  : T1 , T2
        try :
            Apply ()
        except:
            continue
        #Apply
    #perform easy apply operation if True and move to next link if false ***
        time.sleep (60)
    #pass
    
#https://www.linkedin.com/jobs/view/268819011/    
