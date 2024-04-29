from django import forms
from .models import Publisher, Game, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'website']
        labels = {
            'name': _('Name'),
            'website': _('Website'),
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'price', 'release_date', 'publisher', 'type', 'discount', 'image', 'categories', 'description_uk', 'description_fr']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'description_uk': _('Description_uk'),
            'description_fr': _('Description_fr'),
            'price': _('Price'),
            'release_date': _('Release Date'),
            'publisher': _('Publisher'),
            'type': _('Type'),
            'discount': _('Discount'),
            'image': _('Image'),
            'categories': _('Categories'),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': _('Name'),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': _('Username'),
        }