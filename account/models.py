from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    father_name = models.CharField(max_length=100)
    meli_code = models.CharField(max_length=10, unique=True)
    profile = models.ImageField(upload_to="profiles")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "پروفایل ها"
        verbose_name = "پرفایل"
