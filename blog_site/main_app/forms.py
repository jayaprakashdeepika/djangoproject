from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Blog , Profile
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contact_number', 'profile_picture']
