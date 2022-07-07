from django import forms
from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control mb-3"}),
            "content": forms.Textarea(attrs={"class": "form-control mb-3"}),
        }
