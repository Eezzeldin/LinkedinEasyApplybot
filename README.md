# LinkedinEasyApplybot
This bot uses selenium, scrolls through linkedin pages and collects the URLs of the easy apply jobs only and stores them in a sqllite database.It is assumed before on activates this file that he/she has already signed in to their LinkedIn account. Also, it is assumed that the package selenium is already installed and that that google chrome is the web driver used. It would also be worth mentioning that this code has been written for python 2.7. One thing to keep in mind is that I have set the time to get one url link of an easy apply job on linked in to be 2-5 min. and I did this hard constraint to avoid bombarding linkedin servers with my requests. 

#1- Scrapper.py

1.1 Code responsible for scraping easy apply jobs i call the scraper.py , the output of runing this code is a sqllite database that looks like this:

url                                             job Title   JobDescription   Timeonlinkedin  
https://www.linkedin.com/jobs/view/289092819/     XYZ          XYZ               X days


1.2 The operation scheme of Scrapper is described inside the python file. Note that the file must be opened and the operation shceme inside must be followed. This project is not a black box user run yet. Maybe It will never be also.


#2- Applier.py
After the scraper jobs is done. you should open the applier.py and follow its operation scheme described inside. The applier will scroll through the urls scraped by the scraper and starts applying for all the jobs in stored in the sqllite database.



