from blog.models import Post, Category


def recent_posts(request):
    posts = Post.objects.all().order_by("-created")
    categories = Category.objects.all()
    return {
        "recent_posts": posts,
        "category": categories,
    }  # dakhel hameja dastresi dare
