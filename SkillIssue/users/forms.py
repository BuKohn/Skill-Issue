from django import forms

from users.models import Guide


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название руководства'}),
            'content': forms.Textarea(attrs={'placeholder': 'Начните писать ваше руководство здесь...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Введите теги через запятую'}),
        }