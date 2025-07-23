from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment, Message
from django.core.paginator import Paginator
from .forms import MessageForm
from django.http import HttpResponse
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


# Create your views here.
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        body = request.POST.get("message")
        parent_id = request.POST.get("parent_id")

        # بررسی اگر parent_id خالی است، آن را به None تغییر دهیم
        if parent_id == "":
            parent_id = None
        # اگر parent_id
        # موجود باشد، آن را به شیء مربوطه تبدیل می‌کنیم
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        # ایجاد کامنت جدید
        Comment.objects.create(
            comment=body, post=post, user=request.user, parent=parent_comment
        )

    return render(request, "blog/post-details.html", {"post": post})


def post_list(request):
    posts = Post.objects.all()
    page = request.GET.get("page")
    paginator = Paginator(posts, 3)
    object_list = paginator.get_page(page)
    return render(request, "blog/post_list.html", {"posts": object_list})


def category_detail(request, pk):
    category = get_object_or_404(Post, id=pk)
    article = category.article_set.all()
    return render(request, "blog/post_list.html", {"posts": article})


def search(request):
    query = request.GET.get("q")
    articles = Post.objects.filter(title__contains=query)
    page = request.GET.get("page")
    paginator = Paginator(articles, 3)
    object_list = paginator.get_page(page)
    # onaieke havie q riy bozorg hasas  icontaions hasas nist
    return render(
        request, "blog/post_list.html", {"posts": object_list}
    )  # mitavanim az 1 temlate estefade konim dar chand view vali bayad kilid yeki bashe


def contact(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            #     text = form.cleaned_data['text']
            # email = form.cleaned_data['email']
            # title = form.cleaned_data['title']
            # Message.objects.create(text=text, email=email, title=title)

            # mianbor
            form.save()

            return redirect("/")
        else:
            form = ContactForm(request.POST)  # error
    else:
        form = MessageForm()

    return render(request, "blog/contact.html", {"form": form})


@login_required
@require_POST
def like(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "like_count": post.likes.count()})


# class base view
class ListView(View):
    queryset = None
    template_name = None

    def get(self, request):
        return render(request, self.template_name, {"posts": self.queryset})


class Article(ListView):
    queryset = Post.objects.all()
    template_name = "blog/post_list.html"


# template view
class Article2(TemplateView):
    template_name = "blog/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        return context


class HomePageRedirect(RedirectView):
    # baray adres
    # url = 'https://blog.csdn.net/'
    # az name estefade konim
    pattern_name = "blog:list"
    # permanent = 301
    # permanent = 302 = False
    # permanent = True
    # query_string = true ?name=hasti save
    query_string = False

    # adres khas
    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class ArticleDetail(DetailView):
    model = Post
    template_name = "blog/post-details.html"
    # context_object-name= name key


# article_dertail pishfarz khod class

# class PostList(ListView):#def pageinator
#   model = Post
#  template_name = "blog/post_list.html"
# context_object_name = name key in html
# page_
