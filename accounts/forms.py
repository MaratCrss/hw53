from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput)
    email = forms.EmailField(label='email', required=True, widget=forms.EmailInput)
    username = forms.CharField(label='Логин')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        if first_name == '':
            raise forms.ValidationError('Имя не должно быть пустым!!!')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']