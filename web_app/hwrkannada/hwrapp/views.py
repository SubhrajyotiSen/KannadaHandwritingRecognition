from django.http import HttpResponse
from .models import DocumentImage
from django.template import loader
from .models import DocumentImage
from .forms import DocumentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
import subprocess
from .printdoc import unicode_to_kn

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
        return redirect('/hwrapp/results/' + str(image_id), {
                    'image_id' : image_id
            })

    template = loader.get_template('hwrapp/details.html')
    myobject = DocumentImage.objects.get(pk=image_id)
    print (myobject)
    context = {
        'myobject' : myobject,
        'myobjectid' : image_id
    }
    return HttpResponse(template.render(context, request))

"""
    Result page. Needs to be updated to call our HWR module to analyse image
"""
def results(request, image_id):
    template = loader.get_template('hwrapp/results.html')
    output = unicode_to_kn("LWC35C35^35WC48+7C47C42+4WC45+4C39^42C23^41+11C31+2")
    h=html.parser.HTMLParser()
    h.unescape(output)
    context = {
        'output': output
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
                    'image_id' : image.image_id
                })

    # If form data wasnt valid, display empty form again to the user.
    else:
        form = DocumentForm()
    return render(request, 'hwrapp/model_form_upload.html', {
        'form': form
    })
