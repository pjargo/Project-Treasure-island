# Project-Treasure-island

## Sofware Development tool concepts:

### 1. Named Entities Extraction:
  <p> Input: .pdf document </p>
  <p> Output: Rendering of the document text with Named entities extracted </p>
  <li> This is jupyter notebook for processing .pdf documents and html webpages and extracting names entities </li>
  <li> Backend database is SQL </li>
  <li> All data processing is done in python </li>

#### Required Libraries:
    1. Spacy
      Displacy renders the text into the named entity format
    2. Collections
    3. en_core_web_sm
    4. pprint
      Print the outputs as aesthetically pleasing (not required)
    5. tkinter
      Prompt the user to select the disired PDF
    6. PyPDF2
      Parse the pdf
    7. requests
      To get the infomation from the provided url
    8. re
    9. BeautifulSoup
    

  
### 2. Image extraction: 
  <p> Input: Directory of .pdf documents </p>
  <p> Output:Gallary of all the images extracted from the .pdfs </p>
  <li> This is a web-based application developed in Django that extracts all the images from .pdf documents, stores them in a local media foder </li>
  <li> Backend database is SQL </li>
  <li> All data processing is done in python </li>

#### Required Libraries:
    1. Django: Full stack web development framework 
    2. PyMuPDF (fitz) 
      - https://pypi.org/project/PyMuPDF/#files
      - pip install PyMuPDF
    3. from io import BytesIO 
    4. from PIL import Image 
      
      What does PyMuPDF do?
      processes .pdfs and allows user to extract text and images, search for text, render pages, etc.
    
### 3. Mathematical Language Processing:
  Input: .pdf document
  Output:  ...
