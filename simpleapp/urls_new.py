from django.urls import path
from .views_new import (
    NewsList, NewDetail, NewCreate, NewUpdate, NewDelete, NewSearch, subscriptions
)


urlpatterns = [
path('', NewsList.as_view(), name='new_list'),
path('<int:id>', NewDetail.as_view(), name='new_detail'),
path('create/', NewCreate.as_view(), name='new_create'),
path('<int:id>/update/', NewUpdate.as_view(), name='new_update'),
path('<int:id>/delete/', NewDelete.as_view(), name='new_delete'),
path('search/', NewSearch.as_view(), name='new_search'),
path('subscriptions/', subscriptions, name='subscriptions'),
]
