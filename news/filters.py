from django_filters import FilterSet
from .models import Post, Author, Comment
from django.forms import DateInput
from django_filters import FilterSet, CharFilter, \
    ModelMultipleChoiceFilter, DateFilter, \
    ModelChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet, ChoiceFilter



class RequestsFilter(FilterSet):

    class Meta:
        model = Comment
        # fields = ['active']
        fields = {

                'active': ['exact'],
            }




# создаём фильтр
class PostFilter(FilterSet):
    author = ModelChoiceFilter(field_name='author',
                               label='Автор:',
                               lookup_expr='exact',
                               queryset=Author.objects.all()
                               )





    class Meta:
        model = Post
        fields = {
                'author': ['exact'],
                'dateCreation': ['gt'],
                'title': ['icontains'],
                'categoryType': ['exact'],
                'category': ['exact'],


            }


