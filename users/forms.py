from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .models import Profile


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        subject = 'Corrila feedback Submission'
        recipient_email = 'v.linden@mail.ru'  # Replace with the recipient's email address

        # Construct the email message using the form data
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage: {message}"

        # Create and send the email
        # TODO: Add one space between , and [
        email = EmailMessage(subject, email_message,[recipient_email])
        email.send()


class CustomPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add your custom classes to the form fields
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'


# TODO: Remove one empty line. Currently two empty lines to separate classes defined at the top level of the file
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))


class UserProfileCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label="Repeat your password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    occupation = forms.CharField(
        label="Your occupation (optional)",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # TODO: You can use super() directly (Python 3), super(UserProfileCreationForm, self) => Python 2 format
        user = super(UserProfileCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]

        if commit:
            user.save()
            # TODO: Why do we need to create a profile since all of the information are already in User?
            profile = Profile.objects.create(user=user, occupation=self.cleaned_data["occupation"])

        return user


class CorrilaAutnenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
