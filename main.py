import time

import pymongo as pymongo
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait


def save(data):
    collection.insert_one(data)
    print(data)


### Run program ###
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client["mailru"]
collection = db["letters"]

chrome_options = Options()

chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

# get site mail.ru
driver.get('https://mail.ru/')
# driver.find_element(By.XPATH, "//a[@class, 'ph-project svelte-jq5qv5']")
link = driver.find_element(By.XPATH, "//a[contains(@href, '/veoz41')]").get_attribute('href')

#get form for authorization
driver.get(link)

time.sleep(3)
# log-in
elem = driver.find_element(By.CLASS_NAME, "input-0-2-77")
elem.send_keys('gb_students_787')
elem.send_keys(Keys.ENTER)

time.sleep(2)

# input password
# elem = driver.find_element(By.CLASS_NAME, "input-0-2-77")
elem = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div/div/div/form/div[2]/div/div[2]/div/div/div/div/div/input")
elem.send_keys('Gfhjkmlkzcneltynjd001#')
elem.send_keys(Keys.ENTER)

time.sleep(8)

# Getting all mail hrefs
l = driver.find_elements(By.XPATH, "//a[contains(@href, '/inbox')][contains(@class, 'llc_new llc_new-selection js-letter-list-item')]")

time.sleep(1)

def parse(driver, link):

    # get letters page
    driver.get(link.get_attribute('href'))

    # wait page for loading
    time.sleep(5)

    # Reading letter
    # From who
    from_who = driver.find_element(By.XPATH, "//span[contains(@class, 'letter-contact')]")
    # from_who.get_attribute('title')

    # Letter date
    date = driver.find_element(By.CLASS_NAME, 'letter__date')

    # Title of letter
    title_of_mail = driver.find_element(By.CLASS_NAME, 'thread-subject')

    # text message
    m = driver.find_element(By.CLASS_NAME, 'letter-body')
    # print(m.text)

    # dictionary for MongoDB
    letter_dict = {"from": from_who.get_attribute('title'),
                   "date": date.text,
                   "title": title_of_mail.text,
                   "message": m.text
                  }

    print(letter_dict)

    # Save letter_dict to MongoDB
    # save(letter_dict)



# i=0
# # for link in l:
# while True:
#     link = l[i]
#     # link.get_attribute('href')
#     # print(link.get_attribute('href'))
#     # go to each letter
#     time.sleep(3)
#     # driver.get(link.get_attribute('href'))
#     parse(driver, link)
#
#     time.sleep(5)
#     driver.back()
#     time.sleep(3)
#     l = driver.find_elements(By.XPATH, "//a[contains(@href, '/inbox')][contains(@class, 'llc_new llc_new-selection js-letter-list-item')]")
#     # print('-----------links: ',links)
#     # l = links[i:]
#     i+=1
#     # driver.refresh()


i=0
for link in l:
    link = l[i]
    time.sleep(3)
    parse(driver, link)
    time.sleep(5)
    driver.back()
    time.sleep(3)
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/inbox')][contains(@class, 'llc_new llc_new-selection js-letter-list-item')]")
    # print('-----------links: ',links)
    l = links[i:]
    i+=1










# element = driver.find_element(By.CLASS_NAME, "submit-button-wrap")
# //element[contains(@class, 'class1 class2')]
# items = list()
# items = driver.find_elements(By.XPATH, "//a[contains(@class, 'llc llc_normal llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom')]")
# link = driver.find_element(By.XPATH, "//a[contains(@href, '/inbox')][contains(@class, 'llc_new llc_new-selection js-letter-list-item')]").get_attribute('href')
# items = driver.find_elements(By.CLASS_NAME, 'llc llc_normal llc_new llc_new-selection js-letter-list-item js-tooltip-direction_letter-bottom')

# links = driver.find_elements(By.XPATH, "//a[contains(@href, '/inbox/')]")
# link = driver.find_element(By.XPATH, "//a[@href, '/inbox/')]").get_attribute('href')
# i=0
# while links[i] != 0:
# 	print(links[i].text)
# 	i+=1
# //a[contains(@href, '/users/')]").get_attribute('href')
# print()
# //*[@id="root"]/div/div[2]/div/div/div/div/form/div[2]/div/div[2]/div/div/div/div/div/input
# driver.find_element(By.XPATH, "//div[@class,'auto-0-2-80']/input[@name, 'password']")
#
# # elem = driver.find_element(By.ID, 'auto-0-2-80')
# elem = driver.find_element(By.XPATH, "//div[@class, 'auto-0-2-80']/input[@name, 'username']")
# elem.send_keys('gb_students_787')
#
# time.sleep(2)

# driver.get('https://yandex.ru/')
#
# button = driver.find_element(By.CLASS_NAME, "desk-notif-card__login-new-item-title")
# button.click()
# print('!!!')
#
# time.sleep(2)
#
# elem = driver.find_element(By.ID, 'passp-field-login')
# elem.send_keys('alesandrskachkov@yandex.ru')
# elem.send_keys(Keys.ENTER)
#
# time.sleep(2)
#
# elem = driver.find_element(By.ID, 'passp-field-passwd')
# elem.send_keys('StrongFull!')
#
# time.sleep(2)
# button.send_keys(Keys.ENTER)

# button = driver.find_element(By.ID, 'desk-notif-card__mail-title')
# button.send_keys(Keys.ENTER)
#
# time.sleep(2)
#
# button = driver.find_element(By.CLASS_NAME, "Button2 Button2_view_pseudo Button2_size_l PromoOnboardingBeautifulEmail__actionButton--2fgVC")
# button.click()

# ns-view-messages-item-box ns-view-id-98


# link = driver.find_element(By.XPATH, "//a[@href,class='home-link desk-notif-card__login-new-item desk-notif-card__login-new-item_mail home-link_black_yes']")
# button.click()
# print(elem)
# driver.get(link)
# link.click()
# driver.get('https://lenta.com/promo/')
#
# button = driver.find_element(By.CLASS_NAME, "cookie-usage-notice__button-inner--desktop")
# button.click()
#
# driver.implicitly_wait(10)
#
# pages = 0
# while pages < 5:
#     wait = WebDriverWait(driver, 10)
#     button = wait.until(EC.element_to_be_clickable(
#         (
#             By.CLASS_NAME, 'catalog-grid__pagination-button'
#         )
#     ))
#     # button = driver.find_element(By.CLASS_NAME, "catalog-grid__pagination-button")
#     button.click()
#     pages +=1
#     print('page',pages)
#
# items = driver.find_elements(By.CLASS_NAME, 'sku-card-small-container')
# print('page',pages)
# for item in items:
#     name = item.find_element(By.CLASS_NAME, 'sku-card-small-header__title').text
#     rub = item.find_element(By.CLASS_NAME, 'price-label__integer').text
#     cop = item.find_element(By.CLASS_NAME, 'price-label__fraction').text
#     price = float("".join(rub.split()) + '.'+cop)
#     print(name, price)
#
#
# print()
driver.quit()