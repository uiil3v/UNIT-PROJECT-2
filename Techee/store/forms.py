from django import forms
from .models import Product, Comment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['rating','content']
        widgets = {
            'rating': forms.Select(),
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
