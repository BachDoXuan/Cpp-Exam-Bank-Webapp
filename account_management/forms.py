from django import forms

class SignInForm(forms.Form):
    username = forms.CharField(
        label = "username or email",
        max_length = 40,
        min_length = 1,
        error_messages = {
            'required': 'Please enter your username or email',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 1'
        }
    )

    password = forms.CharField(
        label = "password",
        max_length = 40,
        min_length = 8,
        error_messages = {
            'required': 'Please enter your password',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 8'
        }
    )