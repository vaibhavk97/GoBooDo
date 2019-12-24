from fpdf import FPDF
import os
from PIL import Image

class createBook:

    def __init__(self,name,path):
        self.name = name
        self.path = path
        nameList = sorted(os.listdir(os.path.join(path,'Images')),key= lambda x : int(x[:-4]))
        print(nameList)
        self.imageNameList = [os.path.join(path,'Images',x) for x in nameList]

    def makePdf(self):
        firstPath = self.imageNameList[0]
        width, height = Image.open(firstPath).size
        pdf = FPDF(unit="pt", format=[width, height])
        for pagePath in self.imageNameList:
            pdf.add_page()
            pdf.image(pagePath,0,0)
        if not os.path.exists(os.path.join(self.path,'output')):
            os.mkdir(os.path.join(self.path,'output'))
        pdf.output(os.path.join(self.path,'output',str(self.name[:10])+".pdf"),"F")