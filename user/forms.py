from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        max_length=32,
        help_text='First name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        max_length=32,
        help_text='Last name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        max_length=64,
        help_text='Enter a valid email address'
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label='Password Again',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password Again'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        user_email = User.objects.filter(email=email)
        user_uname = User.objects.filter(username=username)

        if user_email:
            raise forms.ValidationError("Email address is already taken")

        if user_uname:
            raise forms.ValidationError("Username is already taken")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label='Username',
    )

    password = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password',
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Wrong username or password entered. Please try again")

        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        return authenticate(username=username, password=password)


class UpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UpdateForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        max_length=32,
        help_text='First name'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        max_length=32,
        help_text='Last name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        max_length=64,
        help_text='Enter a valid email address'
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        user_email = User.objects.filter(email=email)
        user_uname = User.objects.filter(username=username)

        if email != self.user.email:
            if user_email:
                raise forms.ValidationError("Email address is already taken")

        if username != self.user.username:
            if user_uname:
                raise forms.ValidationError("Username is already taken")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
