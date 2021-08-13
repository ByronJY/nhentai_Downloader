import urllib.request as req
import bs4
import time
import os

print("""
               _                _        _ 
         _ __ | |__   ___ _ __ | |_ __ _(_)
        | '_ \\| '_ \\ / _ \\ '_ \\| __/ _` | |
        | | | | | | |  __/ | | | || (_| | |
        |_| |_|_| |_|\\___|_| |_|\\__\__,_|_|
     _                     _                 _           
  __| | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 / _` |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__|
| (_| | (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 \\__,_|\\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|   


====================== Made by ByJY ======================

version: 1.2 (for Linux)
2021/4/23

""")

#取得頁數資訊
def find_pages(lastpage):
    thispage = lastpage.find_next_sibling('div')
    #print(thispage)
    try:
        pages_info = thispage.find('span',{'class':'name'}).string  #本子頁數
    except AttributeError:
        return find_pages(thispage)

    #print(pages_info)
    try:
        pages = int(pages_info)
    except ValueError:
        return find_pages(thispage)
    return pages



#檔案寫入(下載)
def download_pic(picture,path):
    #img = req.urlopen(picture)
    pic = req.urlopen(picture).read()
    path += picture[picture.rfind('.'):]
    #print(path)
    f = open(path,'wb')
    f.write(pic)
    f.close()


while True:

    carNum = input("輸入車號：")
    try:
        folder = os.mkdir("nhentai下載器/Download/" + str(carNum))
    except FileExistsError:
        folder = os.mkdir("nhentai下載器/Download/" + str(carNum) + "(same)")


    topUrl = "https://nhentai.net/g/" + str(carNum)
    print(topUrl)

    #建立一個request物件，附加headers資訊
    request = req.Request(topUrl,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    #解析網頁原始碼
    root = bs4.BeautifulSoup(data,"html.parser")

    #取得本子頁數 pages
    tag_1st = root.find('div','tag-container field-name')
    #print(tag_1st)
    pages = str(find_pages(tag_1st))
    print("共 " + pages + " 頁 (第 0～" + str(int(pages)-1) + " 頁)\n")

    #等待一秒
    time.sleep(0.5)

    #下載每頁之迴圈
    for i in range(int(pages)):
        url = topUrl + "/" + str(i+1)
        print("第 " + str(i) + " 頁 (" + str(i+1) + "/" + str(pages) +")  " + url)

        #建立一個request物件，附加headers資訊
        request = req.Request(url,headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        

        #解析網頁原始碼
        root = bs4.BeautifulSoup(data,"html.parser")

        #尋找圖片
        photo_item = root.find('div',{'id':'content'})
        picture = photo_item.find("img")["src"]
        #print(picture) 純粹註解，檢查程式用

        #呼叫下載圖片
        pic_path = "nhentai下載器/Download/" + str(carNum) + "/" + str(i)
        download_pic(picture,pic_path)
        #等待一秒
        time.sleep(0.5)
    print(str(carNum) + " 下載完成！\n")