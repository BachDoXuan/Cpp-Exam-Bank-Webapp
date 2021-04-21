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

class SignUpForm(forms.Form):
    username = forms.CharField(
        label = "username",
        max_length = 40,
        min_length = 1,
        error_messages = {
            'required': 'Please enter your username',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 1'
        }
    )

    email = forms.CharField(
        label = "email",
        max_length = 40,
        min_length = 1,
        error_messages = {
            'required': 'Please enter your email',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 1'
        }
    )

    firstname = forms.CharField(
        label = "First name",
        max_length = 40,
        min_length = 1,
        error_messages = {
            'required': 'Please enter your first name',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 1'
        }
    )

    lastname = forms.CharField(
        label = "Last name",
        max_length = 40,
        min_length = 1,
        error_messages = {
            'required': 'Please enter your last name',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 1'
        }
    )

    passwd = forms.CharField(
        label = "password",
        max_length = 40,
        min_length = 8,
        error_messages = {
            'required': 'Please enter your password',
            'max_length': 'Max length is 40',
            'min_length': 'Min length is 8'
        }
    )