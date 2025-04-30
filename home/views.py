from django.shortcuts import render
from blog.models import Post
# Create your views here.
# site colorlib baray form login free login
def home(request):
    author = Post.objects.all()
    recent_posts = Post.objects.all()[:3] #global
    for x in recent_posts:
        print(x)
    #recent_post = Post.objects.all().orderby(-created) barsas tarikh joda mishe
    #for post in author:
        #print(post.title)
    return render(request, "homeapp/index.html", context={"author": author})

#nahve estefade az renderpatrial
#def renderpartial(request):
 #   return render(request,'includes/sideBar.html',context={'name':'tag'})

