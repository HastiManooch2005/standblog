from django.urls import path
from . import views
from django.urls import include
app_name = 'blog'
urlpatterns = [
    path('detail/<slug:slug>', views.ArticleDetail.as_view(), name='detail'),
    path('post', views.post_list, name='post'),
    path('art/<int:pk>', views.category_detail, name='category'),
    path('search', views.search, name='search'),
    path('contact', views.contact, name='contact'),
    path('list', views.Article.as_view(), name='list'),
    path('home', views.HomePageRedirect.as_view(), name='home'),
    path('like',views.like, name='like'),
    path('api/v1/',include('blog.api.v1.urls')),

]
