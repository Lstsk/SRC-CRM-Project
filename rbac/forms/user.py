from django import forms
from rbac import models
from django.core.exceptions import ValidationError


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']
        widgets = {'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Passwords did not match')
        return confirm_password


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']
        widgets = {'password': forms.PasswordInput()}

    def __init__(self, *args, **kwargs):
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResetUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']
        widgets = {'password': forms.PasswordInput()}
        labels = {'password': 'Password'}

    def __init__(self, *args, **kwargs):
        super(ResetUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Passwords did not match')
        return confirm_password
