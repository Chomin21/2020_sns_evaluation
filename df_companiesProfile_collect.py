#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time
import datetime
import demoji
import pandas as pd
# 이모지 제거
# demoji.download_codes()
def loginUrl(user_id, user_pw):
    try:
        url = "https://www.instagram.com/"
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        driver.find_element_by_name("username").send_keys(user_id)
        driver.find_element_by_name("password").send_keys(user_pw)
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[3]/button").submit()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div/div/div/button").click()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        insta_account(driver,company_list)
    except:
        print("잘못된 아이디 또는 비밀번호입니다.")


# In[2]:


company_list=[]

f = open("C:/Users/joanl/BAC_project/text/minkyoung.txt", 'r')
company_list = f.readlines()
f.close()


print(company_list)

def insta_account(driver,company_list):
    post = 0
    #이거 꼭 해줘야하는지 잘모르겠음
    url_tmp = driver.current_url
    
    for company in company_list:
        try:
            # 날짜 바꾸기
            codingdate = "2021-03-01"
            
            url = "https://www.instagram.com/{company}/".format(company=company)
            driver.get(url)#성공
        
            userIDList = driver.find_elements_by_css_selector("._7UhW9.fKFbl.yUEEX.KV-D4.fDxYl")
            userID = userIDList[0].text # 아이디

            userInfoList = driver.find_elements_by_css_selector(".g47SY")

            userPost = userInfoList[0] # 게시물 수
            userFollower = userInfoList[1] # 팔로워 수
            userFollowing = userInfoList[2] # 팔로잉 수

            userPostReal = userPost.get_attribute('title')
            userFollowerReal = userFollower.get_attribute('title')
            userFollowingReal = userFollowing.get_attribute('title')

            if userPost.text.find('백') == -1 and userPost.text.find('천') == -1 and userPost.text.find('만') == -1:
                userPost = userPost.text
            else:
                userPost = userPostReal
            if userFollower.text.find('백') == -1 and userFollower.text.find('천') == -1 and userFollower.text.find('만') == -1:
                userFollower = userFollower.text
            else:
                userFollower = userFollowerReal
            if userFollowing.text.find('백') == -1 and userFollowing.text.find('천') == -1 and userFollowing.text.find('만') == -1:
                userFollowing = userFollowing.text
            else:
                userFollowing = userFollowingReal
                
                
            print("- 인스타그램 아이디 : " + userID)
            print("- 팔로워 수 : " + userFollower)
            
            user_profile.loc[post] = [codingdate, url,userID,userPost,userFollower,userFollowing]
            post += 1    
        except:
            continue


# In[3]:


user_profile = pd.DataFrame(columns = ['codingdate','url','id','postnum','followernum','followingnum'])
user_id = "01082417055"
user_pw = "cks3521cks"
loginUrl(user_id, user_pw)
print(user_profile)


# In[4]:


user_profile.to_csv('C:/Users/joanl/BAC_project/text/companies_profile.csv',
                sep=',',
               na_rep='NaN',
                encoding = 'utf-8')


# In[ ]:




