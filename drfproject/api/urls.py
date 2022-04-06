from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns 

urlpatterns=[
    # path('articles', views.article_list), # views.article_list is the defined function
    # path('articles', views.article_details),
    path('articles', views.ArticleAPIView.as_view()), # views.ArticleAPIView is the class defined
    path('articles/<int:pk>', views.ArticleDetailsAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)