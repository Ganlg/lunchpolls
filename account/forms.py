from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Confirm Password')
    birth_date = forms.DateField(required=True, widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'birth_date', 'password', 'password2', ]

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


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=100,widget=forms.PasswordInput, label='Password')

    class Meta:
        model = User
        fields = ('username', 'password')


class EditProfileForm(forms.Form):
    username = forms.CharField(disabled=True, required=False)
    first_name = forms.CharField(max_length=100, label='First Name', required=False)
    last_name = forms.CharField(max_length=100,label='Last Name', required=False)
    birthday = forms.DateField(required=False, widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))