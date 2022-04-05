from dataclasses import fields
from rest_framework import serializers
from .models import Article

# General Serializers (similar to Form)
# class ArticleSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=30)
#     author = serializers.CharField(max_length=50)
#     email = serializers.EmailField(max_length=50)
#     date = serializers.DateField()

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Article.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         # validated data is a Python dictionary, using .get() in dictionary method
#         instance.title = validated_data.get("title", instance.title)
#         instance.author = validated_data.get("author", instance.author)
#         instance.email = validated_data.get("email", instance.email)
#         instance.date = validated_data.get("date", instance.date)
#         instance.save()

#         return instance


# ModelSerializers (similar to modelForm)
# does not do aynthing special, just shorcut for creating serializer class
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title','author','email','date']
        read_only = ['author']
