from fpdf import FPDF
import os
from PIL import Image
from tqdm import tqdm
from pytesseract import image_to_pdf_or_hocr
import PyPDF2
from io import BytesIO

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
        name = str(self.name[:min(10,len(self.name))]).replace(" ","")
        name = ''.join(ch for ch in name if ch.isalnum()) + ".pdf"
        pdf.output(os.path.join(self.path,'Output',name),"F")

    def ocrPdf(self, lang=None):
        pdf = PyPDF2.PdfFileWriter()
        for pagePath in tqdm(self.imageNameList):
            with open(pagePath, 'rb') as ofile:
                im = Image.open(ofile)
                page = image_to_pdf_or_hocr(im, lang=lang)
            pdf.addPage(PyPDF2.PdfFileReader(BytesIO(page)).getPage(0))
        if not os.path.exists(os.path.join(self.path,'Output')):
            os.mkdir(os.path.join(self.path,'Output'))
        name = str(self.name[:min(10,len(self.name))]).replace(" ","")
        name = ''.join(ch for ch in name if ch.isalnum()) + ".pdf"
        with open(os.path.join(self.path,'Output',name),'wb') as ofile:
            pdf.write(ofile)
