from django import forms
from apps.categories.models import Category, Selection
from mptt_autocomplete.widgets import FancyTreeWidget

categories = Category.objects.order_by('tree_id', 'lft')

class SelectionForm(forms.ModelForm):
    class Meta:
        model = Selection
        fields = ('name', 'categories')
        widgets = {
            'categories': FancyTreeWidget(queryset=categories,model=Category)
        }
