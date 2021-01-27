from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.edit import FormView
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from .forms import ImageForm, PdfForm, FileFieldForm
from .models import DispImage, MyImage, FileFieldModel
from mysite.settings import BASE_DIR, MEDIA_URL
from django.utils.datastructures import MultiValueDict
import fitz  # PyMuPDF
import io
from io import BytesIO
from PIL import Image
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.POST)
    obj = ['Select Directory', 'Select Recursive Option. This checks sub-directories', 'Click Submit']
    if request.method == 'POST' and 'load_image' in request.POST:
        form = ImageForm(request.POST, request.FILES)
        file = request.FILES
        print(type(request.FILES))
        print(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('images')
    else:
        form = ImageForm()

    if request.method == 'POST' and 'upload' in request.POST:
        print(request.POST, request.FILES.getlist('files[]'))
        print(request.FILES)
        pdf_form = PdfForm(request.POST, request.FILES)
        print(pdf_form.is_valid())
        if pdf_form.is_valid():
            pdf_form.save()
            return redirect('pdfs')

        for file in request.FILES.getlist('files[]'):
            print(file)
            print(type(file))
            pdf_form = PdfForm(request.POST, file)
            if pdf_form.is_valid():
                pdf_form.save()
        return redirect('pdfs')
    else:
        pdf_form = PdfForm()

    my_context = {'object_list': obj,
                  'form': form,
                  'pdf_form': pdf_form,
                  }
    return render(request, "home.html", my_context)


def success(request):
    return HttpResponse('successfully uploaded')


def display_images(request):
    if request.method == 'GET':
        print(request.GET)
        # getting all the objects in the myImage model
        images = MyImage.objects.all()
        print(images)
        return render(request, 'images2.html', {'images': images, 'total_images': len(images)})


def display_documents(request):
    if request.method == 'GET':
        print(request.GET)
        # Get all the documents from the MyPdf model
        pdfs = FileFieldModel.objects.all()
        print(pdfs)
        return render(request, 'pdfs2.html', {'pdfs': pdfs, 'total_pdfs': len(pdfs)})


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'pdfs.html'  # Replace with your template.
    success_url = 'success'  # Replace with your URL or reverse().

    def __init__(self):
        self.abs_path = str(BASE_DIR) + MEDIA_URL
        self.image_index = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ['Select Directory', 'Select Recursive Option. This checks sub-directories',
                                  'Click Submit']
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'upload' in request.POST:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('file_field')
            if form.is_valid():
                for count, f in enumerate(files):
                    print(f)  # Check to see if the file is a pdf
                    self.handle_uploaded_file(f, count)
                    file_list = self.get_images(str(BASE_DIR) + MEDIA_URL + str(f))
                    # file_list = [self.get_images(str(BASE_DIR) + MEDIA_URL + str(f))]
                    print('file_list', file_list, type(file_list))
                    # I am having some weird tuple issue, temp fix is conditional
                    if file_list is None:
                        continue
                    for file in file_list:
                        if file is not None and type(file) is not tuple and type(file) is not 'NoneType':
                            # imgByteArr = io.BytesIO()
                            # file.save(imgByteArr, format=file.format)
                            # imgByteArr = imgByteArr.getvalue()
                            # file_data = {'img': SimpleUploadedFile(str(f)[:-4], imgByteArr)}
                            # print(file_data)
                            # imageForm = ImageForm({}, file_data)

                            thumb_io = BytesIO()
                            file.save(thumb_io, format='JPEG')
                            thumb_file = InMemoryUploadedFile(thumb_io, None, str(f)[:-4], 'image/jpeg',
                                                              thumb_io.getbuffer().nbytes, None)
                            # request_files = MultiValueDict({'Main_Img': [thumb_file]})
                            # imageForm = ImageForm(request.POST, request_files)
                            # print('request.Post', request.POST, 'request.Files', request_files)
                            # print(type(request_files))
                            # print(imageForm.is_valid())

                            my_image = MyImage()
                            # my_image.Main_Img = file
                            my_image.Main_Img.save('peter' + str(count), thumb_file)
                            # if imageForm.is_valid():
                            #     form.save()
                            # else:
                            #     HttpResponseNotFound('<h1>Page not found</h1>')
                return redirect('images')
                # return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def handle_uploaded_file(self, f, count):
        with open(self.abs_path + str(f), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get_images(self, file):
        pdf_file = fitz.open(file)
        image_list = list()
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
                    image_list.append(image)
                    # return image
            else:
                print("[!] No images found on page", page_index)
        if image_list:
            return image_list
