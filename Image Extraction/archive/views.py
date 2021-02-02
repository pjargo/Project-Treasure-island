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

def display_documents(request):
    if request.method == 'GET':
        print(request.GET)
        # Get all the documents from the MyPdf model
        pdfs = FileFieldModel.objects.all()
        print(pdfs)
        return render(request, 'pdfs2.html', {'pdfs': pdfs, 'total_pdfs': len(pdfs)})