from django.http import HttpResponse
from .models import DocumentImage
from django.template import loader
from .forms import DocumentForm
from django.shortcuts import render
from django.shortcuts import redirect
import html
# Import module here
import os
import sys


rootdir = ""
segdir = ""
augdir = ""
enddir = ""
"""
    Index page. Lists last 6 images that were added to database. 
    Provides option to upload image, the transition between pages(from index to model_form_upload) 
    happens in html file through <a href> tag
"""


def index(request):
    if request.method == 'POST':
        return redirect('/hwrapp/upload/')
    latest_image_list = DocumentImage.objects.order_by('-pub_date')[:6]
    template = loader.get_template('hwrapp/index.html')
    print(latest_image_list)
    context = {
        'latest_image_list': latest_image_list,
    }
    return HttpResponse(template.render(context, request))


"""
    Shows the selected image.
    Provides a button to proceed to analysis of image
"""


def details(request, image_id):
    if request.method == 'POST':
        return redirect('/hwrapp/results/linesegments/' + str(image_id), {
            'image_id': image_id
        })

    template = loader.get_template('hwrapp/details.html')
    myobject = DocumentImage.objects.get(pk=image_id)
    print(myobject)
    context = {
        'myobject': myobject,
        'myobjectid': image_id
    }
    return HttpResponse(template.render(context, request))


"""
    A form to upload image from system.
"""


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            latest_image = DocumentImage.objects.order_by('-pub_date')[:1]
            for image in latest_image:
                print(image.image_id)
                # Use "/" before the path so that the given new path isnt concatenated with present path
                return redirect('/hwrapp/details/' + str(image.image_id), {
                    'image_id': image.image_id
                })

    # If form data wasnt valid, display empty form again to the user.
    else:
        form = DocumentForm()
    return render(request, 'hwrapp/model_form_upload.html', {
        'form': form
    })


"""
    Call for segmentation. Show line segmentation
"""


def linesegments(request, image_id):
    global rootdir, segdir, enddir
    template = loader.get_template('hwrapp/linesegments.html')
    myobject = DocumentImage.objects.get(pk=image_id)
    # Image path of selected image which is to be sent to module for processing
    image_path = myobject.image_url.url
    """
         Call script here for segmentation
    """
    image_path = os.path.join(
        'web_app/hwrkannada/hwrkannada', image_path[1:len(image_path)])

    path = os.path.join(os.path.dirname(__file__), '../../../')
    os.chdir(path)
    sys.path.insert(0, os.getcwd())
    from main import segmentation_call

    rootdir, segdir = segmentation_call(image_path)
    enddir = segdir.split('/images/')[1]
    imagelist = os.listdir(segdir+"/lines")
    imagelist.sort()
    context = {
        'image_id': image_id,
        'enddir': enddir,
        'imagelist': imagelist
    }
    return HttpResponse(template.render(context, request))


"""
    Show word segmentation
"""


def wordsegments(request, image_id):
    global segdir, enddir
    template = loader.get_template('hwrapp/wordsegments.html')
    imagelist = os.listdir(segdir+"/words")
    imagelist.sort()
    context = {
        'image_id': image_id,
        'enddir': enddir,
        'imagelist': imagelist
    }
    return HttpResponse(template.render(context, request))


"""
    Character and ottakshara segmentation
"""


def charsegments(request, image_id):
    global segdir, enddir
    template = loader.get_template('hwrapp/charsegments.html')
    imagelist = []
    for files in os.listdir(segdir):
        if os.path.isfile(os.path.join(segdir, files)):
            imagelist.append(files)
    imagelist.sort()
    print(imagelist)
    context = {
        'image_id': image_id,
        'enddir': enddir,
        'imagelist': imagelist
    }
    return HttpResponse(template.render(context, request))


"""
    Show Augmented characters and ottaksharas
"""


def augmentation(request, image_id):
    global rootdir, segdir, augdir
    template = loader.get_template('hwrapp/augmentation.html')
    myobject = DocumentImage.objects.get(pk=image_id)
    # Image path of selected image which is to be sent to module for processing
    image_path = myobject.image_url.url
    """
         Call script here for segmentation
    """
    image_path = os.path.join(
        'web_app/hwrkannada/hwrkannada', image_path[1:len(image_path)])

    path = os.path.join(os.path.dirname(__file__), '../../../')
    os.chdir(path)
    sys.path.insert(0, os.getcwd())
    from main import augmentation_call

    augdir = augmentation_call(image_path, segdir)
    enddir = augdir.split('/images/')[1]
    imagelist = os.listdir(augdir)
    imagelist.sort()
    context = {
        'image_id': image_id,
        'enddir': enddir,
        'imagelist': imagelist
    }
    return HttpResponse(template.render(context, request))


"""
    Result page. Needs to be updated to call our HWR module to analyse image
"""


def results(request, image_id):
    template = loader.get_template('hwrapp/results.html')

    from main import prediction_call

    output = prediction_call(augdir)
    # The output is parsed and results page is rendered to show the output
    h = html.parser.HTMLParser()
    h.unescape(output)
    myobject = DocumentImage.objects.get(pk=image_id)
    context = {
        'image_id': image_id,
        'myobject': myobject,
        'output': output
    }
    return HttpResponse(template.render(context, request))


def delete_image(request, image_id):
    image = DocumentImage.objects.get(pk=image_id).delete()
    return redirect('/hwrapp/')
