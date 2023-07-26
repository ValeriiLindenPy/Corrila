from django import forms

from .models import Article, Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["first_name", "last_name", "email", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "id": "exampleFormControlTextarea1",
                }
            ),
        }


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "preview_text", "text"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "preview_text": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "preview_text": "Make a preview for your article:",
            "text": "",
        }
