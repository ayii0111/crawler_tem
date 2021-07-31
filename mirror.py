from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup



#把新聞連結（不完整的url），結合成完整的url
def url_href(urlp):
    urlb = 'https://www.mirrormedia.mg'
    return(urlb + urlp)

def sendline(keyword):
    # 資料輸出：若符合關鍵字，則發出line通知
    # 先把爬取的資料都存到變數中
    title1 = '<br>＃' + title_short
    title2 = '<br>＃' + title_long
    title = '<br>＊關鍵字：「{}」<br>＊新聞標題：'.format(keyword) + title1 + title2
    url_ = '＊新聞連結：<br>' + url

    # 以透過ifttt服務送出LINE通知
    url_ifttt = 'https://maker.ifttt.com/trigger/sendLINE/with/key/你的key?value1={}&value2={}'.format(
        title, url_)
    requests.get(url_ifttt)


#打開瀏覽器
dri = webdriver.Chrome('Chromedriver')

title_list = [] #用來儲存爬取過的新聞標題，目的是比對標題是否已經爬取過了，下面會設定最多儲存216則


while True:

    #以瀏覽器打開網頁
    dri.get('https://www.mirrormedia.mg/')
    time.sleep(1)

    #網頁向下滑動2次頁面（因為是動態網頁，往下拉可以增加能夠爬取的新聞數量）
    for x in range(1, 3):
        dri.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    time.sleep(2) #原本以為，隱性等待就可以，結果還是要用到sleep(2)，必須要再研究隱性等待失敗的原因

    '''
    目前最好操作的是css選擇器
    因此把目標資料的元素，都用DevTools去複製它的select，然後去比對差異，進一步可以分析出適當的定位方式
    短標題：
    div.article-gallery > ul > li:nth-child(1) > a > article > div.text-wrapper > h1 > span
    div.article-gallery > ul > li:nth-child(2) > a > article > div.text-wrapper > h1 > span

    每則新聞的區塊：div.article-gallery > ul > li
    短標題：h1 > span
    長標題：div > p
    有連結的區塊：a 
    '''

    soup = BeautifulSoup(dri.page_source, 'lxml') #實測結果BS定位比較不會有額外的坑，缺點有些css、xpath，不被支援
    lis = soup.select('div.article-gallery > ul > li')

    for li in lis:

        title_short = li.select_one('h1 > span').text
        if title_short in title_list:
            continue
        title_list.append(title_short)

        #儲存新聞標題超過設定，每多一則就會刪除舊的一則
        if len(title_list)>100:
            del title_list[0]

        title_long =  li.select_one(' a > article > div.text-wrapper > p').text #此處若直接用selenium的feb方法，無論是css或xpath都會抓錯或抓不到
        href =  li.select_one('a')['href']
        url = url_href(href)
        print(title_short)
        print(title_long)
        print(url)


        keywords = ['台灣','金牌']
        if keywords[0] in title_short:
            if keywords[1] in title_short:
                sendline(keywords[0] +'、'+ keywords[1])
            else:
                sendline(keywords[0])
        elif keywords[1] in title_short:
            sendline(keywords[1])



    time.sleep(15) #15秒用於測試，實際上需求要60秒鐘跑一次迴圈
