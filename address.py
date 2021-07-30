from selenium import webdriver
import time

wd = webdriver.Chrome('chromedriver')
wd.get('https://easymap.land.moi.gov.tw/Index')
time.sleep(2)

# #id值、>標籤[屬性='屬性值']、>標籤~標籤

wd.find_element_by_css_selector("#button_addr").click()
wd.find_element_by_css_selector("#select_city_id1>option[value='C']").click()
time.sleep(1)
wd.find_element_by_css_selector("#select_town_id1>option[value='01']").click()
time.sleep(1)
wd.find_element_by_css_selector("#select_road_id>option[value='中正路']").click()
time.sleep(1)
wd.find_element_by_css_selector("#door_botton").click()
time.sleep(1)

alert = wd.switch_to.alert #切換到alert的彈出視窗
alert.accept() #點擊確認
time.sleep(1)

print(wd.find_element_by_css_selector("#doorListId>ul>li>a").get_attribute("doorplate"))
for ul in wd.find_elements_by_css_selector("#doorListId>ul~ul"):
    print(ul.find_element_by_css_selector("li>a").get_attribute("doorplate"))


wd.close()