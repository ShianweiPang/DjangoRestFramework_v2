from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Article
from .serializers import ArticleSerializer
# from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

# for authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
# at least need to add one permission for session or basic authentication
from rest_framework.permissions import IsAuthenticated

# Class-based view (extends APIView) with authentication
class ArticleAPIView(APIView):
    # it will check the session authentication, if does not exist then only prefer basic authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        articles = Article.objects.all()
        serializers = ArticleSerializer(articles, many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ArticleSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    # Token Authentication
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # getting instance of the article in the models
    def get_article_instance(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        article = self.get_article_instance(pk)
        serializers = ArticleSerializer(article)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        article = self.get_article_instance(pk)
        serializers = ArticleSerializer(article, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        article = self.get_article_instance(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# # Normal Django views 
# # Create your views here.
# @api_view(['GET','POST'])
# def article_list(request):
#     """
#     List all articles, or create a new article.
#     """
#     if request.method =="GET":
#         articles = Article.objects.all()
#         serializers = ArticleSerializer(articles, many=True)
#         return Response(serializers.data)
#     elif request.method=="POST":
#         # request is some sort like this <WSGIRequest: POST '/api/articles'>
#         # the data is in the form of dictionary
#         # data = JSONParser().parse(request) << no need to parse data from the request object of REST framework
#         serializers = ArticleSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET","PUT","DELETE"])
# def article_details(request, pk):
#     """
#     Retrieve, update or delete a article
#     """
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method =="GET":
#         serializers = ArticleSerializer(article)
#         return Response(serializers.data)
#     elif request.method=="PUT":
#         # data = JSONParser().parse(request)
#         # in order to perform and update you need to pass in the instance that you want to update into the constructor
#         # by having partial=True, it allows partial update << Normally this is called PATCH
#         # PUT is replaces all current representations of target resource
#         serializers = ArticleSerializer(article, data=request.data, partial=True)
#         if serializers.is_valid():
#             serializers.save()
#             # The HTTP 204 No Content success status response code indicates that a request has succeeded, 
#             # but that the client doesn't need to navigate away from its current page. (save and continue editting)
#             return Response(serializers.data, status=status.HTTP_204_NO_CONTENT)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method =="DELETE":
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

        

