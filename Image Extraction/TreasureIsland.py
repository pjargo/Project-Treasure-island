import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import re
import PyPDF2
import fitz # PyMuPDF
import io
from PIL import Image

nlp = en_core_web_sm.load()

doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile'
          ' phone market and ordered the company to alter its practices')


# pprint([(X.text, X.label_) for X in doc.ents])
# pprint([(X, X.ent_iob_, X.ent_type_) for X in doc])

def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))


ny_bb = url_to_string(
    'https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage'
    '&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
article = nlp(ny_bb)

# Get a random sentence
sentences = [x for x in article.sents]
print(sentences[22])

# You can only render HTML in a browser and not in a Python console/editor environment.
displacy.render(nlp(str(sentences[20])), jupyter=True, style='ent')


def parsePdf(file):
    with open(file, 'rb') as pdfFileObj:
        # Create the file reader object
        # This operation can take some time, as the PDF stream’s cross-reference tables are read into memory
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        for i in range(int(pdfReader.numPages)):
            pageObj = pdfReader.getPage(i)
            print(pageObj.extractText())
            return pageObj.extractText()


def parsePdf_Image(file):
    with open(file, 'rb') as pdfFileObj:
        # Create the file reader object
        # This operation can take some time, as the PDF stream’s cross-reference tables are read into memory
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)  # Vector check to see if I am reading the expected PDF

        # Get the first page for now
        page0 = pdfReader.getPage(0)
        xObject = page0['/Resources']['/ProcSet'].getObject()
        return xObject


def getImage_pdf(file):
    pdf_file = fitz.open(file)
    pageCount = pdf_file.pageCount
    for page_index in range(pageCount):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image.save(open(f"image{page_index + 1}_{image_index}.{image_ext}", "wb"))


if __name__ == '__main__':
    file = '/Users/peterargo/PycharmProjects/TestPdf.pdf'
    getImage_pdf(file)

    # xObject = parsePdf_Image(file)
    # for obj in xObject:
    #     if xObject[obj] == '/Image':
    #         size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
    #         data = xObject[obj].getData()
    #         if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
    #             mode = "RGB"
    #         else:
    #             mode = "P"
    #
    #         if xObject[obj]['/Filter'] == '/FlateDecode':
    #             img = Image.frombytes(mode, size, data)
    #             img.save(obj[1:] + ".png")
    #         elif xObject[obj]['/Filter'] == '/DCTDecode':
    #             img = open(obj[1:] + ".jpg", "wb")
    #             img.write(data)
    #             img.close()
    #         elif xObject[obj]['/Filter'] == '/JPXDecode':
    #             img = open(obj[1:] + ".jp2", "wb")
    #             img.write(data)
    #             img.close()

    # parsePdf(file)
