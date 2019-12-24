from PIL import Image
import requests
import pickle
from io import BytesIO
import os
import random

class StoreImages:

    def __init__(self,bookpath,proxyflag):
        self.proxyflag = proxyflag
        self.bookPath = bookpath
        self.imagePath = os.path.join(self.bookPath,'Images')
        self.pagesFetched = {}
        self.PageLinkDict = {}
        if not os.path.exists(os.path.join(self.bookPath,'data','pagesFetched.pkl')):
            path = os.path.join(bookpath, 'data', "pageLinkDict.pkl")
            with open(path, 'rb') as ofile:
                self.PageLinkDict = pickle.load(ofile)
        else:
            path = os.path.join(bookpath, 'data', "pagesFetched.pkl")
            with open(path, 'rb') as ofile:
                self.pagesFetched = pickle.load(ofile)

            path = os.path.join(bookpath, 'data', "pageLinkDict.pkl")
            with open(path, 'rb') as ofile:
                allPages = pickle.load(ofile)
            for page in allPages.keys():
                if page not in self.pagesFetched.keys():
                    self.PageLinkDict[page] = allPages[page]
        if not os.path.isdir(self.imagePath):
            os.mkdir(self.imagePath)
        with open('proxies.txt','r') as ofile:
            self.plist = ofile.readlines()

    def getProxy(self):
        prox =  random.choice(self.plist)
        return prox.strip()

    def resethead(self):
        try:
            req = requests.get("https://google.com")
            self.head = {
                'Host': 'books.google.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.00',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'close',
                'Cookie': "NID=" + str(req.cookies['NID']),
            }
        except:
            pass

    def getImages(self,retries):
        self.resethead()
        for page_data in self.PageLinkDict.keys():
                try:
                    link = self.PageLinkDict[page_data]['src']
                    if not link:
                        continue
                    page_number = self.PageLinkDict[page_data]['order']
                    checkIfPageFetched = retries
                    while checkIfPageFetched > 0:
                        if checkIfPageFetched != retries and self.proxyflag :
                            proxy = self.getProxy()
                            proxyDict = {
                                "http": 'http://' + proxy,
                                "https": 'https://' + proxy,
                            }
                            print(f'Using {proxy} for the image of page {page_number}')
                            pageImage = requests.get(link + '&w=1500', headers=self.head,proxies=proxyDict,verify=False)
                        else:
                            pageImage = requests.get(link + '&w=1500', headers=self.head,verify=False)
                        if len(pageImage.content) == 98670:
                            self.resethead()
                            checkIfPageFetched -= 1
                        else:
                            checkIfPageFetched = -1
                            print(f'Fetched image for page {page_number}')
                            self.pagesFetched[page_data]=self.PageLinkDict[page_data]
                            im = Image.open(BytesIO(pageImage.content))
                            im.save(os.path.join(self.imagePath,str(page_number)+".png"))
                    else:
                        if(checkIfPageFetched==0):
                            print("Could not fetch the image of " + str(page_number))
                except Exception as e:
                    print(e)
        with open(os.path.join(self.bookPath,'data','pagesFetched.pkl'),'wb+') as ofile:
            pickle.dump(self.pagesFetched,ofile)