from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Model_Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_post/', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    create_at = models.DateField(auto_now=True)

class Model_File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='document/', null=True, default=None)
    image = models.ImageField(upload_to='image_document/', null=True, blank=True)
    name = models.CharField(max_length=200)
    name_author = models.TextField()
    create_at = models.DateField(auto_now=True)