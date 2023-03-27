from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView

from common.views import CommonContextMixin  # мой миксин
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserSetPasswordForm, UserEmailForm
from users.models import User, EmailVerification
from games.models import BasketItem


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True
    title = 'Авторизация'
    redirect_field_name = 'next'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        redirect = super(UserLoginView, self).form_valid(form)
        if 'basket' in self.request.COOKIES:
            games = self.request.COOKIES['basket'].split()
            for game_id in games:
                BasketItem.objects.create(user_id=self.request.user.id, game_id=game_id, quantity=1)
                print()
            redirect.delete_cookie('basket')
        redirect.set_cookie('is_logged','true', path='/')
        return redirect


class UserLogoutView(LogoutView):

    def get(self, request, *args, **kwargs):
        response = super(UserLogoutView, self).get(request, *args, **kwargs)
        response.delete_cookie('is_logged')
        return response


class ChangePasswordView(PasswordResetView):
    """ Ищем почту в базе пользователей, если нашли отправка email, потом переходит вниз"""
    title = 'Смена пароля'
    template_name = 'users/forgot-password_1_step.html'
    email_template_name = 'users/emails/password_reset_email.html'
    subject_template_name = 'users/emails/reset_subject.txt'
    success_url = reverse_lazy('users:forgot-password-es')
    from_email = settings.EMAIL_HOST_USER
    form_class = UserEmailForm


class ChangePasswordDoneView(PasswordResetDoneView):
    """Страница о том что письмо отправлено"""
    title = 'Письмо отправлено'
    template_name = 'users/forgot-password_2_step.html'


class ChangePasswordConfirmView(PasswordResetConfirmView):
    """Страница полученная из почты. Изменение пароля"""
    form_class = UserSetPasswordForm
    title = 'Подтверждение смены пароля'
    template_name = 'users/forgot-password_3_step.html'
    success_url = reverse_lazy('users:complete-password')


class ChangePasswordCompleteView(PasswordResetCompleteView):
    """Страница о том что пароль изменен"""
    title = 'Пароль изменен'
    template_name = 'users/forgot-password_4_step.html'


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'


class EmailVerificationView(CommonContextMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('index'))


class UserProfileView(CommonContextMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Личный кабинет'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Return the object the view is displaying """
        return self.request.user


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'Личный кабинет',
#         'form': form,
#         'baskets': BasketItem.objects.filter(user=request.user)
#     }
#     return render(request, 'users/profile.html', context)
