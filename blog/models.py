from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils.html import format_html


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "نمونه ها"
        verbose_name = "نمونه"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    body = models.TextField()
    image = models.ImageField(upload_to="images/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    class Meta:
        ordering = ["-created"]
        verbose_name_plural = "مقاله ها"
        verbose_name = "مقاله"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def show_image(self):
        if self.image:
            return format_html(
                '<img src="{}" width="100" height="100" />', self.image.url
            )
        else:
            return "عکس وجود ندارد"

    def total_likes(self):
        return self.likes.count()

    # vabasetegi be request nabashe mitavanim dar model benevisim
    def get_snippet(self):
        return self.body[:100]

    # def get_absolute_api_url(self):
    #   return reverse('blog : api_v1:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


# article.comments.all()  az tarigh article dastresi pyda mikonim be comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", blank=True, null=True
    )  # yani pasokh be on comment
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment[:50]

    class Meta:
        verbose_name_plural = "کامنت"
        verbose_name = "کامنت ها"


class Message(models.Model):
    title = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "پیام ها"
        verbose_name = "پیام"
