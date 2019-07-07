import requests
from io import BytesIO
from multiprocessing import Pool
import time
import asyncio
from proxybroker import Broker
from PIL import Image
from bs4 import BeautifulSoup

class  Goboodo:

    def __init__(self,id,country="co.in"):
        # self.linkMap =
        self.id = id
        self.resethead()
        self.page_count=0

    def getInitialData(self):
        initUrl = "https://books.google.co.in/books?id="+self.id+"&printsec=frontcover"
        page_data = requests.get(initUrl, headers=self.head)
        soup = BeautifulSoup(page_data.content,"html5lib")
        scripts = (soup.findAll('script'))
        print(scripts[6].text)


    def fetchPageLinks(self,page):
        self.b_url = "https://books.google.co.in/books?id="+str(self.id)+"&lpg=RA1-PA141&pg=PT"+ str(page) +"&jscmd=click3"
        page_data = requests.get(self.b_url, headers=self.head)
        return page_data.json()

    def resethead(self):
        req = requests.get("https://google.com")
        self.head = {
            'Host': 'books.google.co.in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.00',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Cookie': "NID=" + str(req.cookies['NID']),
                    }

    def startload(self,page_number, page_json):
        self.resethead()
        for page_data in page_json[u'page']:
            if len(page_data) > 1:
                self.page_count +=1
                try:
                    link = page_data[u'src']
                    print(link)
                    checkIfPageFetched = 0
                    while checkIfPageFetched == 0:
                        pageImage = requests.get(link + '&w=1500', headers=self.head)
                        if len(pageImage.content) == 119974:
                            print("ip limit over on page " + page_number)
                            checkIfPageFetched = 0
                        else:
                            checkIfPageFetched = 1
                            print(f'fetched page {page_number+self.page_count}')
                            im = Image.open(BytesIO(pageImage.content))
                            im.save(str(page_number+self.page_count)+str(page_data['pid']) + ".png")
                except Exception as e:
                    pass
            else:
                break

if __name__ == "__main__":
    elem = Goboodo("AaUzDwAAQBAJ")
    elem.getInitialData()
    i = 1
    # while True:
    #     page_json = elem.fetchPageLinks(i)
    #     print()
    #     for data in page_json[u'page']:
    #         if(len(data))>1:
    #             i+=1
    #             print(data)
    #
    #     print(page_json)
    # elem.startload(0,page_json)
    # print(elem.b_url)