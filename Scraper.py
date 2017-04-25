'''
Hello Job hunter:
=================
Be ready now for massive job application scheme that starts with this code which parses all the detail from linkedin easy apply jobs.
This novel automation mechanism will save you tons of time applying for jobs online.

This piece of code here takes in key words that you would query into linkedin job search bar and it goes page by page capturing the urls and details of eay apply jobs only. Then there will be another piece of code in a
seperate file that will move along these urls one by one and apply for the job  and even put your resume there :) .

Tunable Parameters
==================
You will need to change 3 things to tune this system toward the kind of job you are targeting.
#1- Change the key words of your job search query down there in the scroll () function. I have chosen python to be my search keyword, you choose whatever you like. In addition, I chose the whole united states, you may choose whatever you like.
#2- Everytime you want the scraper to scrape for a different job title and location on linkedin, please remember to change the table name in the sqlite function store () at the very end of the code.
#3- The sleeping time between every scrape operation and the other. Keep in mind please that this project was never intended for aggressive scraping, so respect a time difference of at least 2-3 seconds. The sleep time is on the for loop function Go()

Operation scheme
=================
1- invoke the openbrowser function
2- after the openbrowser function opens a new chrome browser , please login to your linkedin account.
3- invoke the Go () function.... scraping will start...
4- after scraping is over, please invoke the store () function.

Applyer
=======
Thank you very much Sir. Enjoy all of linkedin easy apply jobs in one sqllite database. From here you should refer to the Applyer.py python code to actually use the links in that database and start applying.

The End
=======
Good Luck with your job hunting.

'''



import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sqlite3

def openbrowser():
    global browser
    current_directory = os.getcwd()
    path_to_chromedriver = current_directory + '/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)


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

#the mylist function is called inside the Go() function. mylist function is supposed to get a , b arguments and then return a list that has all the job details.
#mylist function depends on a = getEasyApply_text() and b = getEasyApply_links()
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
          #=====number of pages===================
          counter = counter + 1
          print str (counter)

          #======Unlocking hidden links=============
          #You need to scroll down the whole page here to unveil the hidden easyapply links in the web page. Linkedin seemed to hide em until the user actually scrolls down to see em.
          elem = browser.find_element_by_tag_name('a')
          for i in range (500):
              elem.send_keys (Keys.ARROW_DOWN)

          #======Parsing the links=============================
          a = getEasyApply_text()
          b = getEasyApply_links()
          PythonJobs += mylist (a,b)

          #=======Scrolling Pages============================
          scroll (Pagenumber)

          #========Monitoring Operation from Console===========================
          print "==============" + str(len(b)) +"=Easy Apply jobs Parsed========"

          #========Sleep Time===========================
          time.sleep (5)

#input [joblink , job title]
def store ():
    conn = sqlite3.connect ("linkedin.sqlite")
    cur  = conn.cursor()
    cur.executescript ('''  DROP TABLE IF EXISTS Data ''')
    cur.execute ('''  CREATE TABLE IF NOT EXISTS Data (Joblink VARCHAR , Jobtitle VARCHAR , Company VARCHAR ,Location VARCHAR , Description VARCHAR , Time VARCHAR ) ''')
    #PythonJobs = ['https://www.linkedin.com/jobs/view/289092819/',
    #  'Senior Python Developer, Enterprise Products & Services']
    for joblist in PythonJobs:
         jobtimepost= joblist[5]
         jobdescript= joblist[4]
         joblocation= joblist[3]
         jobcompany = joblist[2]
         myjobtitle = joblist[1]
         myjoblink  = joblist[0]
         cur.execute (''' INSERT INTO Data (Joblink , Jobtitle,Company,Location,Description,Time) VALUES (?,?,?,?,?,?)''' , (myjoblink,myjobtitle,jobcompany,joblocation,jobdescript,jobtimepost))
    #myjoblink  = 'Emad'
    #myjobtitle = 'Senior Python Developer, Enterprise Products & Services'
    conn.commit()
    cur.close()
