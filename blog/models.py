from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE) #har nevisande mitone chand maghale dashte bashe
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    body = models.TextField()
    image = models.ImageField(upload_to='images/')
    created= models.DateTimeField(auto_now_add=True)#tarikh hamon lahze
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
