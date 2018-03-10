# -*-coding:utf-8 -*

########################################################################################################################
# Bot Code
########################################################################################################################

import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary



def launchDriver():
    global browser
    binary = FirefoxBinary('bin/Firefox.app/Contents/MacOS/firefox')
    browser = webdriver.Firefox(firefox_binary=binary, executable_path='bin/geckodriver',log_path='/tmp/geckodriver.log')
    browser.get(('http://www.supremenewyork.com/shop/all/'))

def goToCat(categorie):
    print(categorie)
    browser.find_element_by_xpath('//*[@href="/shop/all/'+categorie+'"]').click()

def selectArticle(categorie, Keywords):
    print(browser.current_url)
    print()
    while browser.current_url == 'http://www.supremenewyork.com/shop/all/'+categorie+'' :
        try:
            art= None
            for kw in Keywords:
                try:
                    art = browser.find_element_by_xpath("//*[text()[contains(.,'"+kw+"')]]")
                    art.click()
                    ActionChains(browser).move_to_element(art).click()
                    print(art.text)
                    break
                except:
                    pass

        except:
            print("No matches, item hasn't dropped yet or you have to select by yourself")
            try:
                WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[text()[contains(.,'"+Keywords[0]+"')]]"))
                )
            except:
                pass
            browser.refresh()
def selectSize():
    try:
        WebDriverWait(browser, 2).until(
          EC.presence_of_element_located((By.ID, 'size'))
     )
        elt = Select(browser.find_element_by_id('size'))
        elt.select_by_visible_text(size)
    except:
        print('size not aviable or item is unisize, default size as been selected')



def monitor():
    print('Monitor Mode')
    soldOut=True
    while soldOut :

        try:
            WebDriverWait(browser, 15).until(
                    EC.presence_of_element_located((By.NAME, 'commit'))
                    )
            soldOut=False
        except:
            browser.refresh()
    browser.find_element_by_name('commit').click()
    browser.find_element_by_xpath('//*[@class="button checkout"]').click()




def checkout():
    while True:
        try:
            if browser.find_element_by_id('order_billing_name').get_attribute("value")=='':

                browser.find_element_by_id('order_email').send_keys(userInfos['email'])
                browser.find_element_by_id('order_billing_name').send_keys(userInfos['name'])
                browser.find_element_by_id('order_tel').send_keys(userInfos['phoneNumber'])
                browser.find_element_by_name('order[billing_address]').send_keys(userInfos['adress']['street'])
                browser.find_element_by_id('order_billing_city').send_keys(userInfos['adress']['city'])
                browser.find_element_by_id('order_billing_zip').send_keys(userInfos['adress']['zip'])
                selectcountry = Select(browser.find_element_by_id('order_billing_country'))
                selectcountry.select_by_visible_text(userInfos['adress']['country'])
                browser.find_element_by_name('credit_card[cnb]').send_keys(userInfos['card']['number'])
                selectMonth = Select(browser.find_element_by_name('credit_card[month]'))
                selectMonth.select_by_visible_text(userInfos['card']['month'])
                selectYear = Select(browser.find_element_by_name('credit_card[year]'))
                selectYear.select_by_visible_text(userInfos['card']['year'])
                browser.find_element_by_name('credit_card[vval]').send_keys(userInfos['card']['ccv'])
                selectBox = browser.find_element_by_id('order_terms')
                ActionChains(browser).move_to_element(selectBox).click().perform()
                browser.find_element_by_name('commit').click()
        except:
            pass

########################################################################################################################
# Gui Code
########################################################################################################################

from appJar import gui

categorie = ''
Keywords = []
size = ''
adress = { 'street' : '', 'city' : '', 'zip': '', 'country': ''}
card = { 'number': '', 'month' : '', 'year' : '', 'ccv' : ''}
userInfos = { 'email': '', 'name' : '', 'phoneNumber' : '', 'adress' : adress, 'card' : card}


app = gui("SupBOT alpha", "600x600")

def press(button):
    userInfos['name'] = app.getEntry("First Name") + ' ' + app.getEntry("Last Name")
    userInfos['phoneNumber'] = app.getEntry("Phone Number")
    userInfos['email'] = app.getEntry("Email")
    userInfos['adress']['street'] = app.getEntry("Adress line 1")
    userInfos['adress']['city'] = app.getEntry("City")
    userInfos['adress']['zip'] = app.getEntry("Postal Code")
    userInfos['adress']['country'] = app.getOptionBox("Country")

    userInfos['card']['number'] = app.getEntry("Card Number")
    userInfos['card']['month'] = app.getOptionBox("month")
    userInfos['card']['year'] = app.getOptionBox("year")
    userInfos['card']['ccv'] = app.getEntry("CCV")

    categorie = app.getOptionBox("category")

    if app.getOptionBox("size") != 'Auto':
        size = app.getOptionBox("size")

    for x in range(1,5):
        if app.getEntry("keyword"+str(x))!='':
            Keywords.append(app.getEntry("keyword"+str(x)))
    print(Keywords)
    launchDriver()
    if categorie !='':
        goToCat(categorie)
    selectArticle(categorie,Keywords)
    selectSize()
    monitor()
    checkout()

app.startLabelFrame("Order Detail")
# these only affect the labelFrame
app.setSticky("ew")
app.setFont(15)
app.addLabelEntry("First Name")
app.addLabelEntry("Last Name")
app.addLabelEntry("Phone Number")
app.addLabelEntry("Email")
app.addLabelEntry("Adress line 1")
app.addLabelEntry("City")
app.addLabelEntry('Postal Code')
app.addLabelOptionBox("Country", ["FRANCE"])
app.stopLabelFrame()


app.startLabelFrame("Visa Detail (Only Visa supported in this version)")
# these only affect the labelFrame
app.setSticky("ew")
app.setFont(15)
app.addLabelEntry("Card Number")
app.addLabelOptionBox("month", ["01","02","03","04","05","06","07","08","09","10","11","12"])
app.addLabelOptionBox("year", ["2018","2019","2020","2021","2022","2023"])
app.addLabelEntry("CCV")
app.stopLabelFrame()



app.startLabelFrame("Item detail")
# these only affect the labelFrame
app.setSticky("ew")
app.setFont(15)
app.addLabelOptionBox("category", ["jackets",'shirts','tops_sweaters','sweatshirts','pants','shorts','hats','bags','accessories','shoes','skate'],0,0)
app.addLabelOptionBox("size", ["Auto","Small","Medium","Large","Xlarge"],1,0)
app.addLabel("keywords", "keywords", 2, 0)
app.addEntry("keyword1",2,1)
app.addEntry("keyword2",2,2)
app.addEntry("keyword3",2,3)
app.addEntry("keyword4",2,4)

app.stopLabelFrame()


app.addButtons(["Submit"], press)
app.go()