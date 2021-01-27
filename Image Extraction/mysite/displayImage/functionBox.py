import tkinter as tk
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
import PyPDF2
import fitz # PyMuPDF
import io
from PIL import Image


def get_pdfs(file_path):
    myPath = file_path + '/'
    print(myPath)
    onlyfiles = list()
    for f in listdir(myPath):
        if (isfile(join(myPath, f)) and f.find('.pdf') != -1):
            onlyfiles.append(join(myPath, f))
        elif not isfile(join(myPath, f)):
            recursive_dir = get_pdfs(join(myPath, f))
            for f1 in recursive_dir:
                onlyfiles.append(f1)
    return onlyfiles


def prompt_user():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()

    pdfs = get_pdfs(folder_selected)
    print(pdfs)


def parsePdf(file):
    # with open(file, 'rb') as pdfFileObj:
        # Create the file reader object
        # This operation can take some time, as the PDF stream’s cross-reference tables are read into memory
    pdfReader = PyPDF2.PdfFileReader(file)
    print(pdfReader.numPages)
    allText = ''
    for i in range(int(pdfReader.numPages)):
        pageObj = pdfReader.getPage(i)
        allText += pageObj.extractText()
    return allText


def parsePdf_Image(file):
    # Create the file reader object
    # This operation can take some time, as the PDF stream’s cross-reference tables are read into memory
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    print(pdfReader.numPages)  # Vector check to see if I am reading the expected PDF

    # Get the first page for now
    page0 = pdfReader.getPage(0)
    xObject = page0['/Resources']['/ProcSet'].getObject()
    return xObject


def get_images(file):
    image_index = 1
    pdf_file = fitz.open(file)
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for img in page.getImageList():
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
            image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
            # increment the image index
            image_index += 1