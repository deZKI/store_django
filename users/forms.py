from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm, \
    PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import User
from .tasks import send_email_verification, send_password_reset


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"
    }))

    def confirm_login_allowed(self, user):
        super(UserLoginForm, self).confirm_login_allowed(user)
        if not user.is_verified_email:
            raise ValidationError(
                _('Почта не подтверждена'),
                code="not_verify",
            )

    class Meta:
        model = User
        fields = ('username', 'password', 'is_verified_email')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя"
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите фамилию"
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите адрес эл. почты"
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Подтверждение пароля"
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Подтверждение пароля"
    }))


class UserEmailForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите адрес эл. почты"
    }))

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        send_password_reset.delay(subject_template_name=subject_template_name,
                                  email_template_name=email_template_name,
                                  context=context, from_email=from_email, to_email=to_email,
                                  html_email_template_name=html_email_template_name)
