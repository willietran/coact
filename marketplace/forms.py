from django import forms
from django.contrib.auth.forms import UserCreationForm
from marketplace.models import *


__author__ = 'WillieTran'


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=30)
    about = forms.CharField(max_length=400,
                            widget=forms.Textarea(attrs={'placeholder': 'Tell a bit about yourself'}))
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirm Password"

    class Meta:
        model = User
        fields = ("username", "name", "email", "password1", "password2", "about", "image")


class LandingForm(forms.Form):
    email = forms.EmailField(min_length=4,
                             widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    name = forms.CharField(min_length=1,
                           widget=forms.TextInput(attrs={'placeholder': 'Name'}))


class CreateClassForm(forms.Form):
    title = forms.CharField(max_length=140,
                            widget=forms.TextInput(attrs={'placeholder': 'Name of Class'}))
    project = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs={'placeholder': 'What are you building?'}))
    short_description = forms.CharField(max_length=160,
                                        widget=forms.Textarea(attrs={'placeholder': 'Brief Summary of Your Class'}))

    description = forms.CharField(min_length=1,
                                  widget=forms.Textarea(attrs={'placeholder': 'Describe your class in detail'}))

    cost = forms.FloatField()
    screenshot = forms.ImageField()


class ReviewForm(forms.Form):
