from django import forms
from django_filters import FilterSet, DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Category


# author =
# создаём фильтр
# class NewsFilter(FilterSet):
# Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
#   class Meta:
#      model = Post
#     fields = ( 'author', 'createTime', 'categoryType')
class NewsFilter(FilterSet):


    createTime = DateFilter(lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Post
        fields = {
        'title':['icontains'],
        'postCategory': ['exact'],
        'author': ['exact' ],

    }
