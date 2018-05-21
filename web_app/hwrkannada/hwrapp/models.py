from django.db import models

# Create your models here.


class DocumentImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_url = models.ImageField(upload_to='documents/')
    pub_date = models.DateTimeField(auto_now=True)
