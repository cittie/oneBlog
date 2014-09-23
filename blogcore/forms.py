from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16)
    password = forms.PasswordInput()