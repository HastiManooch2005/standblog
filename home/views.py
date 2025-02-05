from django.shortcuts import render
from blog.models import Post
# Create your views here.
# site colorlib baray form login free login
def home(request):
    author = Post.objects.all()

    #for post in author:
        #print(post.title)
    return render(request,"homeapp/index.html",context={"author": author})#baray inke html seda zqade shavad...
