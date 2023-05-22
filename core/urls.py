from django.urls import include, path

from .views import *

urlpatterns = [

    path('', ShowHome.as_view(), name='home'),
    path('about/', ShowAbout.as_view(), name='about'),
    path('articles/', ShowArticles.as_view(), name='articles'),
    path('articles/<slug:article_slug>/',
         ShowArticlePage.as_view(), name='article'),
    path('correlate-data/', ShowCorrelation.as_view(), name='correlate'),
    path('correlate-data/error', ErrorView.as_view(), name='error'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('feedback/success', FeedSuccessbackFormView.as_view(), name='success'),
    path('add-article/', CreateArticleView.as_view(), name='add-article'),
]
