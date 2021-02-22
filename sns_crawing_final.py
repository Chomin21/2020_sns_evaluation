#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time
import datetime
import demoji
# 이모지 제거
#demoji.download_codes()
###
def loginUrl(user_id, user_pw):
    try:
        url = "https://www.instagram.com/"
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.get(url)
        time.sleep(2)
        driver.find_element_by_name("username").send_keys(user_id)
        driver.find_element_by_name("password").send_keys(user_pw)
        driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[3]/button").submit()
        time.sleep(3)
        #driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div/div/div/button").click()
        #time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        insta_search(driver, search)
    except:
        print("잘못된 아이디 또는 비밀번호입니다.")
###
def insta_search(driver, search):
    url_tmp = driver.current_url
    url = "https://www.instagram.com/explore/tags/{search}/?hl=ko".format(search=search) # 검색어로 찾기
    driver.get(url)
    time.sleep(2)
    insta_postList(driver)
###
def insta_postList(driver):
    url = driver.current_url
    insta_post_Urls_List = []
    driver.get(url)
    time.sleep(2)
    # 일정 시간동안 스크롤
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds = 120)
    time.sleep(2)
    while True :
        insta_post_Urls = driver.find_elements_by_css_selector(".Nnq7C.weEfm .v1Nh3.kIKUG._bz0w a")
        for urlList in insta_post_Urls:
            insta_post_Urls_List.append(urlList.get_attribute("href"))
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        if datetime.datetime.now() > end:
            break
    insta_post_Urls_List = list(set(insta_post_Urls_List))
    print(len(insta_post_Urls_List))
    insta_accounts(driver,insta_post_Urls_List)
###
def insta_accounts(driver,insta_post_Urls_List):
    company=[]
    for urlList in insta_post_Urls_List:
        driver.get(urlList)
        time.sleep(1)
        try:
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a').click()
            time.sleep(3)
            # 팔로워 수 출력
            userIDList = driver.find_elements_by_css_selector("._7UhW9.fKFbl.yUEEX.KV-D4.fDxYl")
            userID = userIDList[0].text # 아이디
            userInfoList = driver.find_elements_by_css_selector(".g47SY")
            userFollower = userInfoList[1] # 팔로워 수
            userFollowerReal = userFollower.get_attribute('title')
            if userFollower.text.find('백') == -1 and userFollower.text.find('천') == -1 and userFollower.text.find('만') == -1:
                userFollower = userFollower.text
            else:
                userFollower = userFollowerReal
            time.sleep(1)    
            print("\n")
            print("- 인스타그램 아이디 : " + userID)
            print("- 팔로워 수 : " + userFollower)
            print("\n")
            # 소개글
            intro = ""
            try:
                userInfoList = driver.find_elements_by_css_selector(".-vDIg span")
                intro = userInfoList[0].text
                intro = demoji.replace(intro," ")
                print(intro)
            except:
                continue
            # 인증 여부
            checks = ""
            checkList = driver.find_elements_by_css_selector(".Igw0E.IwRSH.eGOV_._4EzTm.soMvl")
            for check in checkList:
                checks = checks + check.text
            #팔로워수 제한
            userFollower = userFollower.replace(',', '')
            if checks.find('인증됨') == -1 and int(userFollower) <= 100000:
                for word in ['문의', '이벤트', '주문', '공구', '협찬', '판매', '마켓', '블로그', '링크', '세일', '할인', '카톡',
                            '카카오톡', '구매', '구입', '다이렉트', '택배', '배송', '제품', '상품', '스토어', '상점', '입금',
                            '플랫폼', 'DM', '디엠', '가격','오픈', 'kakaotalk', 'shop', '쇼핑몰', '샵','open']:
                    if intro.find(word) != -1:
                        company.append(userID)
                        break
        except:
            continue
    add_company(company)
###
def add_company(company):
    # 중복 제거
    f = open("C:/Users/joanl/산학연계 프로젝트/8percent_company_bracelet.txt", 'r')
    lines = f.readlines()
    companyList = company + lines
    companySet = set(companyList)
    f.close()
    # 메모장에 저장
    f = open("C:/Users/joanl/산학연계 프로젝트/8percent_company_bracelet.txt", 'w')
    for account in companySet:
        data = account + "\n"
        f.write(data)
    f.close()
    print(len(companySet))
###
#서안: '마켓', '쇼핑몰', '패션', '이벤트', '블로그마켓', '화장품'
#동두:  '주문제작', '스토어팜', '구제', '데일리룩', '자체제작', '여성의류'
#두유:  '아이폰케이스', '옷가게', '목걸이', '팔찌', '코디', '데일리코디'
#시엔: '베이킹', '맛집', '카페', '핸드메이드', '광고'
hashtagList = ['팔찌']
for hashtag in hashtagList:
    user_id = "01082417055"
    user_pw = "cks3521cks"
    search = hashtag
    loginUrl(user_id, user_pw)


# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pymysql
import time
import datetime
import demoji
# 이모지 제거
demoji.download_codes()
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
        #driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div/div/div/button").click()
        #time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        insta_account(driver,company_list)
    except:
        print("잘못된 아이디 또는 비밀번호입니다.")
company_list=[]
f = open("C:/Users/joanl/산학연계 프로젝트/text/minkyoung.txt", 'r')
company_list = f.readlines()
f.close()
#print(company_list)
#파일 불러왔다 가정하기
#company_list=['sunbaakim']
def insta_account(driver,company_list):
    #이거 꼭 해줘야하는지 잘모르겠음
    url_tmp = driver.current_url
    for company in company_list:
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
        # 소개글
        intro = ""
        try:
            userInfoList = driver.find_elements_by_css_selector(".-vDIg span")
            intro = userInfoList[0].text
            intro = demoji.replace(intro," ")
            print(intro)
        except:
            continue
      #  dbData = [[url,userID,userPost,userFollower,userFollowing,intro]]
      #  connectDB1(dbData)
        insta_post_page(driver)
#한 회사의 게시글 목록 가져오는거..
def insta_post_page(driver):
    url = driver.current_url
    insta_post_Urs=[]
    # 게시글 url 리스트
    insta_post_Urs_List = []
    driver.get(url)
    time.sleep(2)
       # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        insta_post_Urs= driver.find_elements_by_css_selector("._2z6nI .Nnq7C.weEfm .v1Nh3.kIKUG._bz0w a")
        for urlList in insta_post_Urs:
            insta_post_Urs_List.append(urlList.get_attribute("href"))
    # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 1초 대기
        time.sleep(5)
    # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        #순서 섞이긴 하는데 상위 100개가 섞이는 것이다.
        #근데 딱 100개가 잘리는게아님... 3의 배수로 짤림 일단 그건 넘기고..
        insta_post_Url_List = list(set(insta_post_Urs_List))
        # 시험삼아 할때는 20개? 만 해보기=>그래도 맨날 24개나옴
        if len(insta_post_Url_List) >= 20:
            break
#         마지막부분
        if new_height == last_height:
            break
        last_height = new_height
    print(len(insta_post_Url_List))
    insta_post_Info(driver, insta_post_Url_List)  
def insta_post_Info(driver,insta_post_Urs_List):
    for urlList in insta_post_Urs_List:
        driver.get(urlList)
        time.sleep(2)
        try:
            #계정이름
            userID=""
            userID_temp = driver.find_elements_by_css_selector(".sqdOP.yWX7d._8A5w5.ZIAjV")
            userID = userID_temp[0].text
            #위치정보 내용
            locations = ""
            locationsList = driver.find_elements_by_css_selector(".JF9hh")
            for location in locationsList:
                locations = locations + location.text
            #해시태그 내용
            tags = ""
            tagList = driver.find_elements_by_css_selector(".xil3i")
            for tag in tagList:
                tags = tags + tag.text
            #게시글 내용
            Contents = ""
            Content_List = driver.find_elements_by_css_selector(".eo2As .EtaWk .P9YgZ .C4VMK span")
            Content_temp = Content_List[1]
            Contents = Content_temp.text
            #이모티콘 지우는 코드. 위에 import demoji 이용.
            Contents = demoji.replace(Contents," ")
            # 게시글 날짜
            dates = ""
            dateList = driver.find_elements_by_css_selector("._1o9PC.Nzb55")
            for date in dateList:
                date = date.get_attribute('title')
                dates = dates + date 
            #좋아요 수
            likes = ""
            try:
                like_List = driver.find_elements_by_css_selector(".Nm9Fw span")
                likes = like_List[0].text
            except:
                looklike_List = driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div[1]/article/div[3]/section[2]/div/span").click()
                looklike_temp = driver.find_elements_by_css_selector(".vJRqr span")
                likes = looklike_temp[0].text
            print("- url - ")
            print(urlList)
            print("- 계정이름 - ")
            print(userID)
            print("\n- 위치 정보 - ")
            print(locations)
            print("\n- 해시태그 - ")
            print(tags)
            print("\n- 게시글 본문 - ")
            print(Contents)
            print("\n- 작성날짜 - ")
            print(dates)
            print("\n- 좋아요수 - ")
            print(likes)
           # dbData2 = [[urlList,userID,locations,tags,Contents,dates,likes]]
           # connectDB2(dbData2)
        except:
            continue
            
''' phpmyadmin database connecting
#company_profile
def connectDB1(dbData):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    #각자 데이터베이스의 이름
    DB_NAME = '8percent'
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    curs = conn.cursor()
    #테이블이름
    sql = """insert into company_profile(url,id,postnum,followernum,followingnum,intro) values (%s, %s, %s, %s, %s, %s)"""
    curs.executemany(sql, dbData)
    conn.commit()
    conn.close()
def connectDB2(dbData2):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'autoset'
    #각자 데이터베이스의 이름
    DB_NAME = '8percent'
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD,
                       db=DB_NAME, charset='utf8')
    curs = conn.cursor()
    #테이블이름
    sql2 = """insert into company_post(url,id,location,tags,contents,date,likes) values (%s, %s, %s, %s, %s, %s, %s)"""
    curs.executemany(sql2, dbData2)
    conn.commit()
    conn.close()
'''

user_id = "id"
user_pw = "password"
loginUrl(user_id, user_pw)


# In[ ]:


#SQL query
'''
CREATE TABLE `company_profile`(
    `no` INT(20) NOT NULL AUTO_INCREMENT,
    `url` VARCHAR(100) NULL DEFAULT NULL,
    `id` VARCHAR(100) NULL DEFAULT NULL,
    `postnum` VARCHAR(100) NULL DEFAULT NULL,
    `followernum` VARCHAR(100) NULL DEFAULT NULL,
    `followingnum` VARCHAR(100) NULL DEFAULT NULL,
    `intro` VARCHAR(100) NULL DEFAULT NULL,
    PRIMARY KEY(`no`)
    )DEFAULT CHARSET=utf8;

CREATE TABLE `company_post`(
    `no` INT(20) NOT NULL AUTO_INCREMENT,
    `url` VARCHAR(1000) NULL DEFAULT NULL,
    `id` VARCHAR(100) NULL DEFAULT NULL,
    `location` VARCHAR(100) NULL DEFAULT NULL,
    `tags` VARCHAR(1000) NULL DEFAULT NULL,
    `contents` VARCHAR(10000) NULL DEFAULT NULL,
    `date` VARCHAR(100) NULL DEFAULT NULL,
    `likes` VARCHAR(100) NULL DEFAULT NULL,
    PRIMARY KEY(`no`)
    )DEFAULT CHARSET=utf8;
'''

