from django.urls import path

from .views_article import (
    ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, ArticleSearch, subscriptions
)

urlpatterns = [
path('', ArticlesList.as_view(), name='article_list'),
path('<int:id>', ArticleDetail.as_view(), name='article_detail'),
path('create/', ArticleCreate.as_view(), name='article_create'),
path('<int:id>/update/', ArticleUpdate.as_view(), name='article_update'),
path('<int:id>/delete/', ArticleDelete.as_view(), name='article_delete'),
path('search/', ArticleSearch.as_view(), name='article_search'),
]

