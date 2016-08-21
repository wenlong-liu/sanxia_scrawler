# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 23:54:06 2016
@author: Wenlong Liu (wenlongliu@yahoo.com)
This script is used to get water level data from Sanxia.
"""
import requests
import time, random, csv
import datetime
from requests import ReadTimeout, ConnectionError
from bs4 import BeautifulSoup

start_time = time.time()# start time for programs.
     
def get_sanxia_data(date):
    
 #initialize the lists.        
    inflow = list()
    outflow = list()
    inlevel = list()
    outlevel = list()
    
# setup the date and time.
    form_data = {'NeedCompleteTime2' : date  }
    # Get data by post, timeout = 5.
    # Employ Try & except to keep the stability of scrawler.
    try:      
        post = requests.post(url, form_data, timeout = 5)
    except ReadTimeout as e:
            return None 
    except ConnectionError as e:
            return None
    
    # make sure bs4 works well, or return a none.
    try:
        sanxia = BeautifulSoup(post.content, "lxml")
        
        # Sanxia data are instored in a table with class = top_t 
        sanxia_data = sanxia.findAll("table", {"class" : "top_t"})
        # First 4 of the table are inflow, outflow, inlevel and outlevel.
        sanxia_inflow = sanxia_data[1]
        sanxia_outflow = sanxia_data[2]
        sanxia_inlevel = sanxia_data[3]
        sanxia_outlevel = sanxia_data[4]
        # Retrive the data from each tag 'td'.
        for a in sanxia_inflow.findAll('td'):
            b = a.get_text()
            inflow.append(b) 
        for c in sanxia_outflow.findAll('td'):
            b = c.get_text()  
            outflow.append(b)
        for d in sanxia_inlevel.findAll('td'):
            b = d.get_text()
            inlevel.append(b)   
        for e in sanxia_outlevel.findAll('td'):
            b = e.get_text()
            outlevel.append(b)  
    
# remove not useful data, only numbers are what we want.
# as the data in website are in the reverse sorting, we put it back.
        for i in range(7,0,-2):
            inflow_list.append(inflow[i][1:])
            outflow_list.append(outflow[i][1:])
            inlevel_list.append(inlevel[i][1:])
            outlevel_list.append(outlevel[i][1:])
        
        for hour in hour_list:
            time_list.append(str(date + " " + hour + ":00"))  
            
    except AttributeError as e:
            return None
     # Combine the data with a zip object.   
    sanxia_data = zip(time_list, inflow_list, outflow_list,
                      inlevel_list, outlevel_list)
    
    return sanxia_data

def get_Date(start_date, end_date):
    #initialize the lists.
    date_list = list()
    
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_range = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    for date in date_range:
        date_list.append(date.strftime("%Y-%m-%d"))
        
    return date_list
    
def is_Failed(sanxia_data):
    if sanxia_data == None:
        print('Mission failed, store date to failed_date\n')
        failed_date.append(date) # Store the date if failed.
    else:
        print('Finished data on : %s' %date)            
# Randonmly stops for 1 to 5 seconds.    
    random_num = random.randrange(1,5)
    time.sleep(random_num)  
################ program statrs ###########   
hour_list = ('02', '08', '14', '20')
url = "http://www.ctg.com.cn/inc/sqsk.php"

# initialize the lists.
time_list = list()
inflow_list = list()
outflow_list = list()
inlevel_list = list()
outlevel_list = list()
failed_date = list()

# specify the start and end date.
start_date = "2016-08-01"
end_date =   "2016-08-21"   # Acutral end date is 2016-08-20.
date_list = get_Date(start_date, end_date)
# be careful that the end_date should be one day after the actual end-date.

############ loop starts ################
for date in date_list:    
    sanxia_data = get_sanxia_data(date)    
    is_Failed(sanxia_data)
#####　loop ends  #######

# connectwrite the old data in file.
with open("sanxia_scrawler.csv", 'a', newline = "", encoding = 'utf-8') as f:
    writer = csv.writer(f, delimiter = ',')
    for row in sanxia_data:
        writer.writerow(row) 
########## program ends ###############
        
print("mission complete, ^-^ ~\n")
print("-------- %s seconds consumed for scrwaling ---- " %(time.time()- start_time))
