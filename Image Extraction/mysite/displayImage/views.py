from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import MyImage
from mysite.settings import BASE_DIR, MEDIA_URL
import fitz  # PyMuPDF
import io
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
import filetype

# Create your views here.
def success(request):
    return HttpResponse('successfully uploaded')


def display_images(request):
    if request.method == 'GET':
        print(request.GET)
        # getting all the objects in the myImage model
        images = MyImage.objects.all()
        print(images)
        return render(request, 'images2.html', {'images': images, 'total_images': len(images)})


class FileFieldView(FormView):
    """ Class to render the home page view."""
    form_class = FileFieldForm
    template_name = 'pdfs.html'  # Replace with your template.
    success_url = 'success'  # Replace with your URL or reverse().

    def __init__(self):
        self.abs_path = str(BASE_DIR) + MEDIA_URL
        self.image_index = 1
        self.acceptable_files = ['pdf']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ["Select Directory by clicking 'Choose Files' buttton",
                                  'Select Recursive Option. This checks sub-directories',
                                  "Select 'Upload' button",
                                  "You will be re-directed to the image gallery"]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'upload' in request.POST:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            # Delete the contents of the model (table) and the files in the image folder
            MyImage.objects.all().delete()
            self.delete_dir_content(self.abs_path + 'images')
            # Get all of the files that are uploaded, May contain non-PDF files
            files = request.FILES.getlist('file_field')
            if form.is_valid(): # Check if this is needed!***
                for count, f in enumerate(files):
                    # Check the file type, pass if file is PDF
                    guess = filetype.guess(f).extension
                    if guess not in self.acceptable_files:
                        continue
                    # Get the images embedded in the PDF
                    self.handle_uploaded_file(f, count)
                    file_list = self.get_images(str(BASE_DIR) + MEDIA_URL + str(f))
                    # Skip 'None Type' file lists
                    if file_list is None:
                        continue
                    # Iterate through each file, save the image in dir and database
                    for idx, file in enumerate(file_list):
                        if file is not None and type(file) is not tuple and type(file) != 'NoneType':
                            # Save image in 'media/image' dir, convert to bytes and save to memory
                            thumb_io = BytesIO()
                            file.save(thumb_io, format='JPEG')
                            thumb_file = InMemoryUploadedFile(thumb_io, None, str(f)[:-4].replace('.', ''), 'image/jpeg',
                                                              thumb_io.getbuffer().nbytes, None)
                            # Instantiate model and save image in the database, need to instantiate here
                            my_image = MyImage()
                            my_image.Main_Img.save(str(f)[:-4] + '_image' + str(idx), thumb_file)
                return redirect('images')
            else:
                return self.form_invalid(form)

    def delete_dir_content(self, mydir):
        filelist = [f for f in os.listdir(mydir)]
        for f in filelist:
            os.remove(os.path.join(mydir, f))

    def handle_uploaded_file(self, f, count):
        with open(self.abs_path + str(f), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get_images(self, file):
        """Extract the images from the PDF document"""
        pdf_file = fitz.open(file)
        full_image_list = list()
        for page_index in range(len(pdf_file)):
            # get the page itself
            page = pdf_file[page_index]
            image_list = page.getImageList()
            # printing number of images found in this page
            if image_list:
                print(f"[+] Found a total of {len(image_list)} image(s) in page {page_index}")
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
                    image.save(
                        open(f"{self.abs_path}/images/image{page_index + 1}_{self.image_index}.{image_ext}", "wb"))
                    # increment the image index
                    self.image_index += 1
                    full_image_list.append(image)
            else:
                print("[!] No images found on page", page_index)
        if image_list:
            return full_image_list
        return None