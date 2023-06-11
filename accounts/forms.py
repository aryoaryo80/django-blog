from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=255, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        max_length=255, label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1, password2 = self.cleaned_data['password1'], self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            return ValidationError('password and confirm password do not match')
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            return ValidationError('this username already exists')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        help_text='<a href="../password/">change password</a>')

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name', 'biography', 'email',
                  'phone_number', 'is_active', 'is_admin')


class UserCreationForm(forms.Form):
    username = forms.CharField(label='username or email',
                               max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='username or email',
                               min_length=1, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
                                min_length=1, max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                min_length=1, max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        password1, password2 = self.cleaned_data['password1'], self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            return ValidationError('password and confirm password do not match')
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            return ValidationError('this username already exists')
        return password2

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return ValidationError('this username already exists')
        return super().clean()


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'age',
                  'phone_number', 'biography')
        widgets = {
            "full_name": forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
