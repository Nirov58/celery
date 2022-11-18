from django.urls import path
from .views import *


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('category/<int:pk>', NewsInCategory.as_view(), name='news_category'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    path('<int:pk>', NewsItem.as_view(), name='news_item'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('limit/', news_limit, name='news_limit'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]
