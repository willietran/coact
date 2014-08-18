from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from marketplace.models import *


__author__ = 'WillieTran'


class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    about = forms.CharField(max_length=400,
                            widget=forms.Textarea(attrs={'placeholder': 'Tell a bit about yourself'}))
    image = forms.ImageField(required=True)
    occupation = forms.CharField(max_length=30,
                                 required=True,)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password2'].label = "Confirm Password"

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2", "about", "image", "occupation")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(u'Email Addresses Must Be Unique.')


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

    cost = forms.DecimalField(decimal_places=2, max_digits=10)
    screenshot = forms.ImageField(required=True)


class ReviewForm(forms.Form):
    review = forms.CharField(max_length=140,
                             widget=forms.Textarea(attrs={'placeholder': 'Write a short review for others!'}))
    # content = forms.CharField(max_length=400,
    #                           widget=forms.TextInput(attrs={'placeholder': 'Write Your Review'}))
