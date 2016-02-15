import csv
from urllib import request
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#商品名
#JANコード
#価格（税込み）
#在庫（在庫がない場合は注文ボタン上に別途表示）
#獲得ポイント
#URL

def search(url):
    try:
        response = request.urlopen(url)
        body = response.read()
        # Parse HTML
        soup = BeautifulSoup(body, "lxml")
    except:
        return ["", "", "", "", ""]
    # get product name
    try:
        name = soup.find(class_='i-cname').find('h1').string
    except:
        name = "NoName"
    # get product JAN code
    try:
        jcode = soup.find(class_='i-cname').findAll('li', text=re.compile(r'.*JANコード.*'))[0].string[8:-1]
    except:
        jcode = '0'
    #if len(jcode) < 13:
    #    [0]*(13 - len(jcode)).append(jcode) # 先頭に０のリスト付加
    # get price (including tax)
    #price = soup.find(class_='i-cprice').findAll('small')[0].string[5:-1]
    try:
        i_price = soup.find(class_='i-cprice').findAll("small", text=re.compile(r'^\(税込.*'))[0].string[5:-1]
    except:
        price = '0'
    # get whether it has stock or not
    stock = isStocked(soup)
    # get points
    try:
        points = soup.find(class_='i-cpts').find('em').string
    except:
        points = '0'
    # write to csv file
    return [name, jcode, price, stock, points]

def isStocked(soup):
    stock = soup.find(class_="i-cpts").find('strong')
    if isinstance(stock, type(None)):
        return "在庫なし"
    else:
        return "在庫あり"

def writeCSV(source):
    f = open('data.csv', 'a')
    csvWriter = csv.writer(f)
    csvWriter.writerow(source)
    f.close()

def getProductURLs(url):
    urls = []
    base_url = 'http://www.ecj.jp/'
    response = request.urlopen(url)
    body = response.read()
    # Parse HTML
    soup = BeautifulSoup(body, "lxml")
    box_names = soup.find_all(class_='s-box-name-name1')
    for box in box_names:
        urls.append(base_url + box.find("a").attrs['href'])
    return urls
'''
def scrollAndGetURLs(url):
    urls = []
    base_url = 'http://www.ecj.jp'
    browser = webdriver.Chrome()
    
    browser.get(url)
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    # loop to bottom
    flag = True
    i = 0
    num = 0
    while flag:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        i = i + 1
        if i % 10 == 0:
            items = browser.find_elements_by_class_name("s-box-name")
            num1 = len(items)
            if num1 > num:
                num = num1
            elif num1 == num:
                time.sleep(2.0)
                items = browser.find_elements_by_class_name("s-box-name")
                num1 = len(items)
                elem.send_keys(Keys.PAGE_DOWN)
                if num1 == num:
                    time.sleep(6.0)
                    items = browser.find_elements_by_class_name("s-box-name")
                    elem.send_keys(Keys.PAGE_DOWN)
                    num1 = len(items)
                    if num1 == num:
                        flag = False

    boxes = browser.find_elements_by_class_name("s-box-name-name1")
    for box in boxes:
        urls.append(box.find_element_by_tag_name('a').get_attribute('href'))
    return urls
'''
