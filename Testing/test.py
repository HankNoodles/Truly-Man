import requests
import os
import re
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

replyOver18 = {
    'from': '/bbs/Beauty/index.html',
    'yes' : 'yes' 
}

folder_root = './Download/'
if os.path.exists(folder_root) == False:
    os.makedirs(folder_root)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
#TODO choose the source forum, and then make folder if it is not exist.
#

folder_source = folder_root + 'PTT/'
if os.path.exists(folder_source) == False:
    os.makedirs(folder_source)

session = requests.session()
response = session.post("https://www.ptt.cc/ask/over18", verify="./certs.pem", data=replyOver18) #Skip the age-verify page
if response.status_code == requests.codes.ok:
    #TODO Parsing the whole article list, and dealing with those selected articles.
    # Invalid: annoucement, help finding, too much negative comments
    #
    response = session.get("https://www.ptt.cc/bbs/Beauty/M.1584533842.A.6AB.html", headers=headers)
    if response.status_code == requests.codes.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('a', string=re.compile("^https://i.imgur.com")) #Get those imgur picture
        if items:
            #title = soup.find("meta",  property="og:title")["content"]
            #arthur, board, title, datetime
            infos = soup.find_all(class_ = "article-meta-value")
            for i, info in enumerate(infos):
                if i == 0: 
                    arthur = ''.join(info.contents)
                if i == 1: 
                    board = ''.join(info.contents)
                if i == 2: 
                    title = ''.join(info.contents)
                if i == 3: 
                    datetime = ''.join(info.contents)

            folder_path = folder_source + board + '/[' + datetime + '] ' + title + '/'
            if os.path.exists(folder_path) == False:
                os.makedirs(folder_path)

            for index, item in enumerate(items):
                if item:
                    html = requests.get(item.get('href'))
                    img_name = 'photo' + str(index+1) + '.jpg'
                    image = Image.open(BytesIO(html.content))
                    image.save(folder_path+img_name, "JPEG")
            print(title + " download completed!")
        else:
            #TODO those photos might be stored in the other space.
            print("The other file space is not supported.")
    else:
        print("Can not access web page")
else:
    print("Can not access web page")
