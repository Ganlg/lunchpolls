from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password2']


class ChangePassword(forms.Form):
    current_password = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Current Password')
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput, label='New Password')
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Confirm Password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['new_password'] != cd['new_password2']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['new_password2']