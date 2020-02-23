from fpdf import FPDF
import os
from PIL import Image
from tqdm import tqdm

class createBook:

    def __init__(self,name,path):
        self.name = name
        self.path = path
        nameList = sorted(os.listdir(os.path.join(path,'Images')),key= lambda x : int(x[:-4]))
        self.imageNameList = [os.path.join(path,'Images',x) for x in nameList]

    def makePdf(self):
        firstPath = self.imageNameList[0]
        width, height = Image.open(firstPath).size
        pdf = FPDF(unit="pt", format=[width, height])
        for pagePath in tqdm(self.imageNameList):
            pdf.add_page()
            pdf.image(pagePath,0,0)
        if not os.path.exists(os.path.join(self.path,'Output')):
            os.mkdir(os.path.join(self.path,'Output'))
        pdf.output(os.path.join(self.path,'Output',str(self.name[:min(10,len(self.name))])+".pdf"),"F")