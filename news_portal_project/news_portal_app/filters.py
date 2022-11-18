from django_filters import FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter
from django.forms.widgets import DateInput, CheckboxSelectMultiple
from .models import Post, Category


class NewsFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Title')
    date = DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gte',
        label='Not older than'
    )
    author__user__username = CharFilter(lookup_expr='icontains', label='Author')
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(),
        label='Categories'
    )

    class Meta:
        model = Post
        fields = ['category', 'name', 'author__user__username', 'type', 'date']
