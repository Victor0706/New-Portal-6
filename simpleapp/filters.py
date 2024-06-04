from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import New, Article


class NewFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='added_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       model = New
       fields = {
           'title': ['icontains'],
           'category': ['icontains'],
           'added_at': ['gt'],
       }

class ArticleFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='added_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
       model = Article
       fields = {
           'title': ['icontains'],
           'category': ['icontains'],
           'added_at': ['gt'],
       }