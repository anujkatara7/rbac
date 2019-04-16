from django import forms
from .models import User


class RegisterationForm(forms.ModelForm):
    use_required_attribute = False
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = '__all__'
