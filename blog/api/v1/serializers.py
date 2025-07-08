from rest_framework import serializers
from ...models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source='get_snippet')
    #relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True)
    #absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('slug','created')
        #category = serializers.SlugRelatedField(many = False,queryset = Category.objects.all(), slug_field='name')
        #def get_absolute_url(self,obj):
            #request = self.context.get('request')
            #return request.build_absolute_url(obj)
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        #request = self.context.get('request')
        #print(request.__dict__)
        #if request.parser_context.get('kwargs').get("pk"):
         #   rep.pop('snippet')
        rep ['category'] = CategorySerializer(instance.category.all(),many=True).data
        return rep