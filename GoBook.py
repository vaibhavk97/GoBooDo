import json
import random
import requests
from bs4 import BeautifulSoup


class  Goboodo:

    def __init__(self,id,country="co.in"):
        self.id = id
        self.resethead()
        self.page_count=0
        self.pageLinkDict = {}
        self.pageList = []
        self.lastCheckedPage = ""
        self.obstinatePages = []

    def createPageDict(self,jsonResponse):
        for pageData in jsonResponse[0]['page']:
            self.pageList.append(pageData['pid'])
            self.pageLinkDict[pageData['pid']]={}
            self.pageLinkDict[pageData['pid']]['src'] = ""
            self.pageLinkDict[pageData['pid']]['order'] = pageData['order']

    def getInitialData(self):
        initUrl = "https://books.google.co.in/books?id="+self.id+"&printsec=frontcover"
        page_data = requests.get(initUrl, headers=self.head)
        soup = BeautifulSoup(page_data.content, "html5lib")
        scripts = (soup.findAll('script'))
        stringResponse = ("["+scripts[6].text.split("_OC_Run")[1][1:-2]+"]")
        jsonResponse = json.loads(stringResponse)
        self.createPageDict(jsonResponse)
        for elem in jsonResponse[3]['page']:
            page = elem['pid']
            self.pageList.remove(page)
            self.pageLinkDict[page]['src'] = elem['src']

    def insertIntoPageDict(self, subsequentJsonData):
        if(len(self.pageList)==0):
            return False
        for pageData in subsequentJsonData['page']:
            if('src' in pageData.keys() and pageData['src']!=""):
                lastPage = pageData['pid']
                self.pageLinkDict[lastPage]['src'] = pageData['src']
                try:
                    self.pageList.remove(lastPage)
                except Exception as e:
                    pass
        return True

    def fetchPageLinks(self,proxy=None):
        self.resethead()
        if(proxy):
            proxy = "https://"+proxy
            proxyDict = {
                "http": proxy,
                "https": proxy,
            }
            self.b_url = "https://books.google.co.in/books?id=" + str(self.id) + "&pg=" + str(self.pageList[0]) + "&jscmd=click3"
            page_data = requests.get(self.b_url, headers=self.head,proxies=proxyDict)
            return page_data.json()
        else:
            self.b_url = "https://books.google.co.in/books?id="+str(self.id)+"&pg="+ str(self.pageList[0]) +"&jscmd=click3"
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
    # def getProxy(self):


if __name__ == "__main__":
    book = Goboodo("NWTwBQAAQBAJ")
    book.getInitialData()
    interimData = book.fetchPageLinks()
    lastFirstList = book.pageList[0]
    maxPageLimit = 0
    maxPageLimitHIT = 4
    proxyFlag = 0
    while True:
        if (proxyFlag):
            print("using proxy")
            interimData = book.fetchPageLinks("wjvglned-"+str(random.randint(10,800))+":pdlm9oshnhe9@p.webshare.io:80")
        else:
            interimData = book.fetchPageLinks()
        book.insertIntoPageDict(interimData)
        print(book.pageList)
        if(maxPageLimit == book.pageList[0]):
            maxPageLimitHIT-=1
        if(maxPageLimitHIT==0):
            maxPageLimitHIT = 4
            book.obstinatePages.append(book.pageList[0])
            book.pageList = book.pageList[1:]
            print("Check_limit_exceeded")
            print(book.pageLinkDict)
        if(lastFirstList==book.pageList[0]):
            maxPageLimit = lastFirstList
            proxyFlag = 1
        else:
            proxyFlag = 0
        lastFirstList = book.pageList[0]

