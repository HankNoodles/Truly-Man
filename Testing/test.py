import requests
import os
from bs4 import BeautifulSoup

replyOver18 = {
    'from': '/bbs/Beauty/index.html',
    'yes' : 'yes' 
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
session = requests.session()
response = session.post("https://www.ptt.cc/ask/over18", verify="./certs.pem", data=replyOver18)
if response.status_code == 200:
    response = session.get("https://www.ptt.cc/bbs/Beauty/M.1584533842.A.6AB.html", headers=headers)
    if response.status_code != 200:
        print("Can not access web page")
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())
        folder_path = './photo'
        if os.path.exists(folder_path) == False:
            os.makedirs(folder_path)
        items = soup.find_all('meta', property="og:description")
        #for item in items:
            #print(item["content"])
            #print(soup.get_text())
else:
    print("Can not access web page")
