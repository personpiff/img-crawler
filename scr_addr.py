import requests
from bs4 import BeautifulSoup
from PIL import Image
import os
import time
import json

def main():
    try:
        with open("addr.json","w") as f:
            addr_dicts=dict()
            for i in range(0,170):
                try:
                    addr_dicts[i]=get_img_addr_from_page("https://www.shzx.org/a/143-5969-%d.html"%i,i+1)
                    time.sleep(0.1)
                except:
                    pass
            json.dump(addr_dicts,f)
    except:
        pass

def download_img(iurl,fname):
    print("Img dl from %s"%iurl)
    try:
        resp=requests.get(iurl,stream=True)
        content_size=int(resp.headers['content-length'])
        has_data=0
        tpercent=0
        with open(fname,"wb") as f:
            for chunk in resp.iter_content(chunk_size=None):
                f.write(chunk)
                has_data+=len(chunk)
                cpercent=100.0*has_data/content_size
                if cpercent-tpercent>10:
                    tpercent=cpercent
                    print("Pic %s: %.2f%%."%(fname,tpercent))
        targ_fname=(os.path.splitext(fname))[0]+".jpg"
        with Image.open(fname) as im:
            im.save(targ_fname)
        print("Pic %s: Status %d."%(fname,resp.status_code))
        os.system("del %s"%fname)
    except Exception as excp:
        # raise excp
        print(excp)
        # print("Errdl")
        # print(excp)
        # return

def get_img_from_page(pageurl,id):
    print("Start pic %d"%id)
    try:
        resp=requests.get(pageurl)
        resp.encoding="utf-8"
        print("Pic %d's page:%d"%(id,resp.status_code))
        htmlt=resp.text
        soup=BeautifulSoup(htmlt,'html.parser')
        thediv=soup.find_all("div",class_="picture")[0]
        download_img(thediv.p.img["src"],"%d.webp"%id)
    except Exception as excp:
        # raise excp
        print(excp)
    #     print("ERr")
    #     print(excp)
    #     return

def get_img_addr_from_page(pageurl,id):
    try:
        resp=requests.get(pageurl)
        resp.encoding="utf-8"
        print("Pic %d's page:%d"%(id,resp.status_code))
        htmlt=resp.text
        soup=BeautifulSoup(htmlt,'html.parser')
        thediv=soup.find_all("div",class_="picture")[0]
        return thediv.p.img["src"]
    except Exception as excp:
        # raise excp
        print(excp)
    #     print("ERr")
    #     print(excp)
    #     return

if __name__=="__main__":
    main()
