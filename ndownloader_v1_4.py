import urllib
import urllib.request as req
import bs4
import time
import os
import platform

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

version: 1.4 (Windows/Linux/Android/iPhone)
2022/1/23

""")

# 取得頁數資訊
def find_pages(lastpage):
    thispage = lastpage.find_next_sibling('div')
    #print(thispage)
    try:
        pages_info = thispage.find('span',{'class':'name'}).string  # 本子頁數
    except AttributeError:
        return find_pages(thispage)

    #print(pages_info)
    try:
        pages = int(pages_info)
    except ValueError:
        return find_pages(thispage)
    return pages


# 檔案寫入(下載)
def download_pic(picture,path):
    #img = req.urlopen(picture)
    pic = req.urlopen(picture).read()
    path += picture[picture.rfind('.'):]
    #print(path)
    f = open(path,'wb')
    f.write(pic)
    f.close()


# 檢查路徑是否存在，若不存在則建立
def cheak_dir(dir, SLASH):
    try:
        folder = os.mkdir(dir + SLASH +"Download")
    except FileExistsError:
        pass


# 取得解析後的HTML
def get_HTML(url):
    # 建立一個request物件，附加headers資訊
    request = req.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75"
    })
    try:
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 404
        else:
            print("HTTP error: " + e.code)
            return -1

    # 解析網頁原始碼
    return bs4.BeautifulSoup(data,"html.parser")

# 前置作業
# 判斷作業系統，切換分隔符
SLASH = "/"
if platform.system() == "Windows":
    SLASH = "\\"
elif platform.system() == "Linux":
    SLASH = "/"
elif platform.system() == "Darwin":
    SLASH = "/"
else:
    print("本程式可能不支援你的作業系統")

#NOW_DIR = os.path.abspath(os.getcwd())
NOW_DIR = os.path.dirname(os.path.realpath(__file__))
DIR = NOW_DIR + SLASH + "Download" + SLASH
cheak_dir(NOW_DIR, SLASH) # 檢查路徑是否存在


while True:

    carNum = input("輸入車號：")

    topUrl = "https://nhentai.net/g/" + str(carNum)
    print(topUrl)

    # 解析網頁原始碼
    root = get_HTML(topUrl)
    if root == 404:
        print("查無此車！\n")
        continue
    elif root == -1:
        continue

    try:
        folder = os.mkdir(DIR + str(carNum))
    except FileExistsError:
        print("存在相同檔案！\n")
        continue

    # 取得本子頁數 pages
    tag_1st = root.find('div','tag-container field-name')
    #print(tag_1st)
    pages = str(find_pages(tag_1st))
    print("共 " + pages + " 頁 (第 0～" + str(int(pages)-1) + " 頁)\n")

    # 等待
    time.sleep(0.5)

    # 下載每頁之迴圈
    for i in range(int(pages)):
        page_url = topUrl + "/" + str(i+1)
        #print("第 " + str(i) + " 頁 (" + str(i+1) + "/" + str(pages) +")  " + url)
        print(f"第{i:>3} 頁 ({i+1:>2}/{pages:<2})  " + page_url)

        # 解析網頁原始碼
        root = get_HTML(page_url)

        # 尋找圖片
        photo_item = root.find('div',{'id':'content'})
        picture = photo_item.find("img")["src"]
        #print(picture)

        # 呼叫下載圖片
        pic_path = DIR + str(carNum) + SLASH + str(i)
        download_pic(picture,pic_path)
        # 等待
        time.sleep(0.5)
    
    print(str(carNum) + " 下載完成！\n")