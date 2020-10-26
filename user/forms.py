from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django import forms


# User Registration Form
class RegistrationForm(UserCreationForm):
    # Username field
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    # First name field
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        max_length=32,
        help_text='First name'
    )

    # Last name field
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        max_length=32,
        help_text='Last name'
    )

    # Email field
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        max_length=64,
        help_text='Enter a valid email address'
    )

    # Password Field
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )

    # Password Again Field
    password2 = forms.CharField(
        label='Password Again',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password Again'})
    )

    def clean(self):
        """
        Clean and check for validity of the form
        """

        # Fetch cleaned email and username data.
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        # Fetch possible user objects from the database
        # based on provided and email and password.
        user_email = User.objects.filter(email=email)
        user_uname = User.objects.filter(username=username)

        # If user exists based on the email address or username,
        # raise validation error.
        if user_email:
            raise forms.ValidationError("Email address is already taken")

        if user_uname:
            raise forms.ValidationError("Username is already taken")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)


class UpdateForm(forms.ModelForm):

    # Constructor
    def __init__(self, *args, **kwargs):

        # Get the user object from kwargs
        self.user = kwargs.pop('user', None)
        super(UpdateForm, self).__init__(*args, **kwargs)

    # Username field
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    # First name field
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        max_length=32,
        help_text='First name'
    )

    # Last Name field
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        max_length=32,
        help_text='Last name'
    )

    # Email field
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        max_length=64,
        help_text='Enter a valid email address'
    )

    def clean(self):
        """
        Clean and check for validity of the form
        """

        # Getting cleaned email and username data.
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        # Get possible user objects based on email and username.
        user_email = User.objects.filter(email=email)
        user_uname = User.objects.filter(username=username)

        # If the user has changed his email
        # and if the email already exists.
        if email != self.user.email:
            if user_email:
                raise forms.ValidationError("Email address is already taken")

        # If the user has changed his username
        # and if the username already exists.
        if username != self.user.username:
            if user_uname:
                raise forms.ValidationError("Username is already taken")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class DeleteAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []
