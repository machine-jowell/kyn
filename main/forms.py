from multiprocessing import Event
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, UserEvent
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit, Fieldset

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age', 'contactNo', 'address', 'neighbourhood')

class UserAuthenticationForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username", "password")

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']


class UserEditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = {"email"}
    
    def save(self, commit=True):
        user = super(UserEditProfile, self).save(commit=False)
        user.email = self.cleaned_data['email']
    
        if commit:
            user.save()
        return user

class UserProfileEditProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("contactNo", "address", "neighbourhood", "profile_image")
    
    def save(self, commit=True):
        user = super(UserProfileEditProfile, self).save(commit=False)
        user.contactNo = self.cleaned_data['contactNo']
        user.address = self.cleaned_data['address']
        user.neighbourhood = self.cleaned_data['neighbourhood']
        user.profile_image = self.cleaned_data['profile_image']

        if commit:
            user.save()
        return user

class UserChangePassword(forms.ModelForm):
    class Meta:
        model = User
        fields = {"password"}
        labels = {'password': 'New Password'}
        widgets = {
            'password': forms.PasswordInput()
        }

class EventCreationForm(forms.ModelForm):

    class Meta:
        model = UserEvent
        fields = ("name", "description", "location", "category", "date", "start_time", "end_time", "event_image")
        labels = {
            'name': 'Name of Event',
            'description': 'Description of the Event (Word Limit, 400 chars)',
            'date': 'Date of Event (YYYY-MM-DD)',
            'start_time': 'Start Time of Event (HH:MM)',
            'end_time': 'End Time of Event (HH:MM)',
            'event_image': 'Image of the Event (Attach 1)',
        }
        widgets = {
            'description': forms.TextInput(attrs={'style':'height:6em'}),
            'date': forms.TextInput(attrs={'type': 'date', 'style': 'max-width:7em'}),
            'start_time': forms.TextInput(attrs={'type': 'time', 'style': 'max-width:7em'}),
            'end_time': forms.TextInput(attrs={'type': 'time', 'style': 'max-width:7em'})
        }

class EventEditForm(forms.ModelForm):
    class Meta:
        model = UserEvent
        fields = ("name", "description", "location", "category", "date", "start_time", "end_time", "event_image")
        labels = {
            'name': 'Name of Event',
            'description': 'Description of the Event (Word Limit, 400 chars)',
            'date': 'Date of Event (YYYY-MM-DD)',
            'start_time': 'Start Time of Event (HH:MM)',
            'end_time': 'End Time of Event (HH:MM)',
            'event_image': 'Image of the Event (Attach 1)',
        }
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'start_time': forms.TextInput(attrs={'type': 'time'}),
            'end_time': forms.TextInput(attrs={'type': 'time'})
        }
    
    
        





