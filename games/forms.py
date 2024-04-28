from django import forms
from .models import Publisher, Game, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'website']


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'release_date', 'publisher', 'type', 'discount', 'image', 'categories']

        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']