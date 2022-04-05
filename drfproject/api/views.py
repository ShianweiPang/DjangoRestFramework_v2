from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def article_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method =="GET":
        articles = Article.objects.all()
        serializers = ArticleSerializer(articles, many=True)
        return JsonResponse(serializers.data, safe=False)
    elif request.method=="POST":
        # request is some sort like this <WSGIRequest: POST '/api/articles'>
        # the data is in the form of dictionary
        data = JSONParser().parse(request)
        serializers = ArticleSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        return JsonResponse(serializers.errors, status=400)

@csrf_exempt
def article_details(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method =="GET":
        serializers = ArticleSerializer(article)
        return JsonResponse(serializers.data, safe=False)
    elif request.method=="PUT":
        data = JSONParser().parse(request)
        # in order to perform and update you need to pass in the instance that you want to update into the constructor
        # by having partial=True, it allows partial update << Normally this is called PATCH
        # PUT is replaces all current representations of target resource
        serializers = ArticleSerializer(article, data=data, partial=True)
        if serializers.is_valid():
            serializers.save()
            # The HTTP 204 No Content success status response code indicates that a request has succeeded, 
            # but that the client doesn't need to navigate away from its current page. (save and continue editting)
            return JsonResponse(serializers.data, status=204)
        return JsonResponse(serializers.errors, status=400)
    elif request.method =="DELETE":
        article.delete()
        return HttpResponse(status=204)

        

