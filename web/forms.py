from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from web.models import User, Course, Comment, RatingStar, Rating


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input your firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input your secondname'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input your username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Input your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Input your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'tags', 'price', 'text', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-input'}),
        }


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)
