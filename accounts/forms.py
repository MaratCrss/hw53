from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import widgets
from accounts.models import Profile


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput)
    email = forms.EmailField(label='email', required=True, widget=forms.EmailInput)
    username = forms.CharField(label='Логин')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name == '' and last_name == '':
            raise forms.ValidationError('Имя или фамилия не должно быть пустым!!!')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'email': 'Email'}
        widgets = {
            'first_name': widgets.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': widgets.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': widgets.EmailInput(attrs={'class': 'form-control mb-3'})
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['github', 'about', 'avatar']
        widgets = {
            'github': widgets.TextInput(attrs={'class': 'form-control mb-3'}),
            'about': widgets.Textarea(attrs={'class': 'form-control mb-3'}),
            'avatar': widgets.ClearableFileInput(attrs={'class': 'form-control mb-3'})
        }


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']