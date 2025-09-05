from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserPhoto


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',
                  'gender', 'age', 'city', 'hobbies', 'status')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'age', 'city',
                  'hobbies', 'status', 'is_private')
        widgets = {
            'hobbies': forms.Textarea(attrs={'rows': 4}),
        }

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = UserPhoto
        fields = ['photo', 'description', 'is_main']
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'Описание фото...',
                'class': 'form-control'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }