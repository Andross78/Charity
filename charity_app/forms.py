from django import forms
from django.contrib.auth import get_user_model

from .models import Donation, Category

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email','password','first_name','last_name']
        widgets = {'password': forms.PasswordInput}
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "Hasła nie są identyczne!"
            )


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email','password']
        widgets = {'password': forms.PasswordInput}

categories = Category.objects.all()
CATEGORY = [(cat.id,cat.name) for cat in categories]

class AddDonatForm(forms.Form):
    bags = forms.IntegerField()
    institution = forms.CharField()
    address = forms.CharField()
    phone = forms.CharField(max_length=64)
    city = forms.CharField(max_length=64)
    postcode = forms.CharField(max_length=64)
    data = forms.DateField()
    time = forms.TimeField()
    more_info = forms.CharField()
    category = forms.MultipleChoiceField(choices=CATEGORY)


class UserEditForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

class MailForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    message = forms.CharField()