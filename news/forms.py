from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment
from django.contrib.auth.models import User
from .models import Profile



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white', 
                'rows': 3, 
                'placeholder': 'Напишите комментарий...'
            }),
        }

# Форма для данных аккаунта
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Форма для данных профиля
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']