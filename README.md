# Project-Treasure-island

## Sofware Development tool concepts:

1. Named Entities Extraction:
  <p> Input: .pdf document </p>
  <p> Output: Rendering of the document text with Named entities extracted </p>
  
2. Image extraction: 
  <p> Input: Directory of .pdf documents </p>
  <p> Output:Gallary of all the images extracted from the .pdfs </p>
  * This is a web-based application developed in Django that extracts all the images from .pdf documents, stores them in a local media foder
  * Backend database is SQL
  * All data processing is done in python

### Required Libraries:
    1. Django: Full stack web development framework 
    2. PyMuPDF (fitz) 
      - https://pypi.org/project/PyMuPDF/#files
      - pip install PyMuPDF
    3. from io import BytesIO 
    4. from PIL import Image 
      
      What does PyMuPDF do?
      processes .pdfs and allows user to extract text and images, search for text, render pages, etc.
    
3. Mathematical Language Processing:
  Input: .pdf document
  Output:  ...
