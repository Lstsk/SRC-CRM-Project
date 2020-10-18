from django import forms
from rbac import models
from django.utils.safestring import mark_safe


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'icon': forms.RadioSelect(
                choices=[
                    ['fa-file-zip-o', mark_safe('<i class="fa fa-file-zip-o " aria-hidden="true"></i>')],
                    ['fa-gear', mark_safe('<i class="fa fa-gear " aria-hidden="true"></i>')]
                ]
            )
        }


class SecondMenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        exclude = ['pid']

    def __init__(self, *args, **kwargs):
        super(SecondMenuModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),

        }


class MultiAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    menu_id = forms.ChoiceField(
        choices=[(None, '------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    pid_id = forms.ChoiceField(
        choices=[(None, '-------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.all().values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')




class MultiEditPermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )  # 获取用户id，进行修改操作
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    menu_id = forms.ChoiceField(
        choices=[(None, '------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    pid_id = forms.ChoiceField(
        choices=[(None, '-------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid_id__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')

