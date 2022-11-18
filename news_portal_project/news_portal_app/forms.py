from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from .models import Post


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'text',
            'author',
            'category'
        ]
        widgets = {'category': CheckboxSelectMultiple}
