
# coding: utf-8

# In[1]:


"""
Created for NITRR's Result website crawling
Date: Dec 18, 2018
author: devp
"""


# In[2]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
import csv
import pandas as pd


# In[3]:


browser = webdriver.Firefox()


# In[4]:


start_roll_no = '16118001'
expected_no_of_students = 85

# for 90(sliders) series
#start_roll_no = '16118901'
#expected_no_of_students = 10

filename = 'IT_BTech_5th_Sem'


# In[5]:


url_addr = "https://results.nitrr.ac.in/Default.aspx"


# In[6]:


browser.get(url_addr)


# In[7]:


roll_no = start_roll_no
for x in range(expected_no_of_students):
    roll_no_find = browser.find_element_by_id("txtRegno")
    roll_no_find.clear()
    roll_no_find.send_keys(roll_no)
    btnimgShow_find = browser.find_element_by_id("btnimgShow")
    btnimgShow_find.click()
    
    lblSName_find = browser.find_elements_by_id("lblSName")
    
    if len(lblSName_find)>0: #for handling student not available or result not published case
        WebDriverWait(browser,8).until(EC.presence_of_element_located((By.ID,'ddlSemester')))
        #the above wait for giving sufficient time to load the page for select drop-down menu
        select_sem = Select(browser.find_element_by_id("ddlSemester"))
        try:
            select_sem.select_by_value('5') # for handling students not in 5th Sem (eg. Rollno 48)
            show_result_find = browser.find_element_by_id("btnimgShowResult")
            show_result_find.click()
            WebDriverWait(browser,6).until(EC.presence_of_element_located((By.ID,"lblSPI")))
            # the below cannot be done yet (page doesn't load fully and text is extracted
            # resulting in duplicate texts)
            #stu_name_find = browser.find_element_by_id("lblStudentName")
            #stu_name = stu_name_find.text
            spi_find = browser.find_element_by_id("lblSPI")
            spi = spi_find.text
            cpi_find = browser.find_element_by_id("lblCPI")
            cpi = cpi_find.text

            dict_stu_details={
                'Roll_no':roll_no,
                'SPI':spi,
                'CPI':cpi
                }

            roll_no = str(int(roll_no)+1)
            with open(filename,'a+', newline='') as csvfile:
                fieldnames = ['Roll_no',
                             'SPI',
                             'CPI'
                             ]
                writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
                writer.writerow(dict_stu_details)
        except NoSuchElementException:
            roll_no = str(int(roll_no)+1)
            pass
        
    else:
        roll_no = str(int(roll_no)+1)
        stu_not_found_alert_box = browser.switch_to_alert()
        stu_not_found_alert_box.accept()


# In[8]:


# to make a spreadsheet instead of text document
df = pd.read_csv(filename,header=None)
df.rename(columns={0:'RollNo',1:'SPI',2:'CPI'},inplace=True)
df.to_csv(filename+'_final.csv',index=False)

