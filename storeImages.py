import pytesseract
from PIL import Image
import requests
import pickle
from io import BytesIO
import os
import random

class StoreImages:

    def __init__(self,bookpath,proxyflag,resolution,tesserPath):
        self.pageResolution = resolution
        self.proxyFlag = proxyflag
        self.bookPath = bookpath
        self.tesserPath = tesserPath
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
                'Cookie': "__Secure-ENID=" + str(req.cookies['__Secure-ENID']),
            }
        except:
            pass

    def pageEmpty(self,image):
        im = Image.open(BytesIO(image))
        width, height = im.size
        im = im.resize((int(width / 5), int(height / 5)))
        gray = im.convert('L')
        bw = gray.point(lambda x: 0 if x < 250 else 255, '1')
        try:
            text = pytesseract.image_to_string(bw)
        except:
            pytesseract.pytesseract.tesseract_cmd = self.tesserPath
            text = pytesseract.image_to_string(bw)
        return text.replace('\n', " ") == 'image not available'


    def getImages(self,retries):
        self.resethead()
        for pageData in self.PageLinkDict.keys():
                try:
                    link = self.PageLinkDict[pageData]['src']
                    if not link:
                        continue
                    pageNumber = self.PageLinkDict[pageData]['order']
                    checkIfPageFetched = retries
                    while checkIfPageFetched > 0:
                        proxyFailed = False
                        if checkIfPageFetched != retries and self.proxyFlag :
                            proxy = self.getProxy()
                            proxyDict = {
                                "http": 'http://' + proxy,
                                "https": 'https://' + proxy,
                            }
                            print(f'Using {proxy} for the image of page {pageNumber}')
                            proxyFailed = False
                            try:
                                pageImage = requests.get(link + '&w=' + str(self.pageResolution), headers=self.head, proxies=proxyDict, verify=False)
                            except:
                                print('Could not connect with this proxy')
                                proxyFailed = True
                        else:
                            pageImage = requests.get(link + '&w=' + str(self.pageResolution), headers=self.head, verify=False)
                        if self.pageEmpty(pageImage.content) or proxyFailed:
                            self.resethead()
                            checkIfPageFetched -= 1
                        else:
                            checkIfPageFetched = -1
                            print(f'Fetched image for page {pageNumber}')
                            self.pagesFetched[pageData]=self.PageLinkDict[pageData]
                            im = Image.open(BytesIO(pageImage.content))
                            im.save(os.path.join(self.imagePath,str(pageNumber)+".png"))
                    else:
                        if(checkIfPageFetched==0):
                            print("Could not fetch the image for page " + str(pageNumber))
                except Exception as e:
                    print(e)
        with open(os.path.join(self.bookPath,'data','pagesFetched.pkl'),'wb+') as ofile:
            pickle.dump(self.pagesFetched,ofile)
