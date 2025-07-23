from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
)
from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .page import DefaultPagination

"""@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)  # gharare koli item dashte bashe
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)"""


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":  # update etelat
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=204)


class PostList1(ListCreateAPIView):  # ham get ham post
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer  # form tamiz tare
    queryset = Post.objects.all()


"""class PostList1(GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer  # form tamiz tare
    queryset = Post.objects.all()
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)"""

"""bayad queryset befrestim
class PostList1(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer  # form tamiz tare
    queryset = Post.objects.all()


    def get(self, request):
        queryset = self.get_queryset()
        serializer =serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)"""


class PostList(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer  # form tamiz tare

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        return Response(status=204)


# ghabeliat update dare RetrieveUpdateAPIView
class PostDetail2(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = (
        Post.objects.all()
    )  # همه پست‌ها را می‌دهد و فیلتر کردن بر اساس slug خودکار انجام می‌شود
    lookup_field = "slug"


class PostDetail1(
    GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"  # yani donbal che objectiam

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, slug):
        post = Post.objects.get(slug=slug)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.delete()
        return Response(status=204)


# viewset
"""class PostViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    #list post
    def list(self,request,*args,**kwargs):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    #detail post
    def retrieve(self,request,slug):
        post = Post.objects.get(slug=slug)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self,request,slug):
        post = Post.objects.get(slug=slug)
        post.delete()

        return Response(status=204)
    def update(self,request,slug):
        post = Post.objects.get(slug=slug)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()"""


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["category", "author"]
    search_fields = ["title"]
    ordering_fields = ["created"]
    pagination_class = DefaultPagination
    # yani ye mored ezafe
    # @action(detail=True, methods=['get'])
    # ef get_ok(self,request):
    #   return Response({'detail':'ok'})


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
