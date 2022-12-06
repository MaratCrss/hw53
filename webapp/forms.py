from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import IssueModel, ProjectModel
import re


class TaskWithProjectForm(forms.ModelForm):
    class Meta:
        model = IssueModel
        fields = ['title', 'status', 'type', 'content']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control mb-3',
                                              'placeholder': 'Название задачи'}),
            'status': widgets.Select(attrs={'class': 'form-control mb-3'}),
            'type': widgets.CheckboxSelectMultiple,
            'content': widgets.Textarea(attrs={'class': 'form-control mb-3', 'rows': 6,
                                               'placeholder': 'Основной Текст'})
        }

    regular_int = "\\d"
    html_tags_regular = r'([<>].+?[</>])'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 50:
            raise ValidationError('Название не должно быть больше 40 символов')
        if re.match(self.regular_int, title):
            raise ValidationError('В названии должны быть только буквы')
        if re.findall(self.html_tags_regular, title):
            raise ValidationError('В названии не должны быть знаков "<" или ">", "/", ">"')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 1000:
            raise ValidationError('Текст не должен быть больше 900 символов')
        if re.match(self.regular_int, content):
            raise ValidationError('В Описании должны быть только буквы')
        if re.findall(self.html_tags_regular, content):
            raise ValidationError('В Описании не должны быть знаков "<" или ">", "/", ">"')
        return content


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False,
                             widget=widgets.TextInput(attrs={'class': 'form-control mb-3 w-50 d-inline-block', 'placeholder': 'Название задачи'}))


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['title', 'content', 'created_at', 'updated_at']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control mb-3',
                                              'placeholder': 'Название проекта'}),
            'created_at': widgets.DateInput(attrs={'class': 'form-control mb-3'}),
            'updated_at': widgets.DateInput(attrs={'class': 'form-control mb-3'}),
            'content': widgets.Textarea(attrs={'class': 'form-control mb-3', 'rows': 6,
                                               'placeholder': 'Основной Текст'})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = IssueModel
        fields = ['title', 'project', 'status', 'type', 'content']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control mb-3',
                                              'placeholder': 'Название задачи'}),
            'status': widgets.Select(attrs={'class': 'form-control mb-3'}),
            'project': widgets.Select(attrs={'class': 'form-control mb-3'}),
            'type': widgets.CheckboxSelectMultiple,
            'content': widgets.Textarea(attrs={'class': 'form-control mb-3', 'rows': 6,
                                               'placeholder': 'Основной Текст'})
        }