from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from posts.models import PostFlag

class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'username',
            'status',
            'image_url',
            'facebook_link',
            'twitter_link',
            'instagram_link',
            'location',
            'about_me'
            ]

# Flag Form
class FlagForm(forms.ModelForm):
    other = forms.CharField(required=False)
    class Meta:
        model = PostFlag
        fields = [
            'category',
            'other'
        ]
