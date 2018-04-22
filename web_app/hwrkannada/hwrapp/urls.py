from django.urls import path

from . import views

urlpatterns = [
	# /hwrapp/
	path('', views.index, name='index'),
	# /hwrapp/details/image_id
	path('details/<int:image_id>/', views.details, name='details'),
	# /hwrapp/results/image_id
	path('results/<int:image_id>', views.results, name='results'),
	# /hwrapp/upload
	path('upload/',views.model_form_upload, name = 'model_form_upload')
]
