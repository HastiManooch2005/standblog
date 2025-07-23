from .views import (
    post_detail,
    PostList,
    PostDetail,
    PostList1,
    PostViewSet,
    CategoryViewSet,
)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("post_set", PostViewSet)  # 1.kodom viewset 2.basename = name
router.register("category", CategoryViewSet)
app_name = "api_v1"
urlpatterns = [
    path("post1/", PostList.as_view(), name="blog_list"),
    path("post/detail/<slug:slug>", PostDetail.as_view(), name="detail"),
    path("post2/", PostList1.as_view(), name="blog_list1"),
    path(
        "setview/",
        PostViewSet.as_view({"get": "list", "post": "create"}),
        name="setview1",
    ),  # in get = method list
    path(
        "setview/<slug:slug>",
        PostViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="setview2",
    ),
]
urlpatterns += router.urls
