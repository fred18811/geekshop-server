from django import forms

from users.models import User
from users.forms import UserRegistrationForm, UserProfileForm

from products.models import Product, ProductsCategory

class UserAdminRegistrationForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))


class ProdactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Имя продукта'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control py-4', 'placeholder': 'Описание'}))
    price = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Цена'}))
    quantitly = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Колличество'}))
    category = forms.ModelChoiceField(queryset=ProductsCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantitly', 'category', 'image')
