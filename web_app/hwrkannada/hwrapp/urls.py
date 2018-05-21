from django.urls import path

from . import views

urlpatterns = [
    # /hwrapp/
    path('', views.index, name='index'),
    # /hwrapp/details/image_id
    path('details/<int:image_id>/', views.details, name='details'),
    # /hwrapp/results/image_id
    path('results/<int:image_id>', views.results, name='results'),
    # /hwrapp/results/linesegments/image_id
    path('results/linesegments/<int:image_id>',
         views.linesegments, name='linesegments'),
    # /hwrapp/results/wordsegments/image_id
    path('results/wordsegments/<int:image_id>',
         views.wordsegments, name='wordsegments'),
    # /hwrapp/results/charsegments/image_id
    path('results/charsegments/<int:image_id>',
         views.charsegments, name='charsegments'),
    # /hwrapp/results/augmentation/image_id
    path('results/augmentation/<int:image_id>',
         views.augmentation, name='augmentation'),
    # /hwrapp/upload
    path('upload/', views.model_form_upload, name='model_form_upload'),
    # /hwrapp/delete_image/image_id
    path('delete_image/<int:image_id>',
         views.delete_image, name='delete_image')
]
