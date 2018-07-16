from django import forms
from django.contrib.auth.models import User
from hub.models import *


class RegisterForm(forms.ModelForm):
    ''' Register Form '''
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta():
        model = User
        fields = ('username', 'password', 'repeat_password', 'first_name', 'last_name', 'email')


class ResumeForm(forms.ModelForm):
    ''' Reseme Form (Dashboard) '''
    class Meta():
        model = UserProfile
        fields = ('resume_file', 'description')


class ChangePasswordForm(forms.Form):
    ''' Change Password Form '''
    current_password = forms.CharField(required=True, widget=forms.PasswordInput())
    new_password = forms.CharField(required=True, widget=forms.PasswordInput())
    repeat_new_password = forms.CharField(required=True, widget=forms.PasswordInput())


class ChangeProfilePicForm(forms.ModelForm):
    ''' Change Profile Picture Form '''
    class Meta():
        model = UserProfile
        fields = ('picture',)


class CommentForm(forms.ModelForm):
    ''' Comment Form '''
    class Meta():
        model = Comment
        fields = ('content',)
        widgets = {
          'content': forms.Textarea(attrs={'rows':2, 'cols':50}),
        }