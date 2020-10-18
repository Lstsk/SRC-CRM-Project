
from django import forms
from rbac.models import UserInfo


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = UserInfo
        fields = ('name', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("Passwords Did Not Match")