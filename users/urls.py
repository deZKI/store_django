from django.urls import path

from users.views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, EmailVerificationView, \
    ChangePasswordView, ChangePasswordDoneView, ChangePasswordConfirmView, ChangePasswordCompleteView, WishListView

app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view(),  name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/wishlist/', WishListView.as_view(), name='wishlist'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password/reset/', ChangePasswordView.as_view(), name='forgot-password'),
    path('password/reset/start', ChangePasswordDoneView.as_view(), name='forgot-password-es'),

    path('password/reset/confirm/<uidb64>/<token>/', ChangePasswordConfirmView.as_view(), name='change-password'),
    path('password/reset/done', ChangePasswordCompleteView.as_view(), name='complete-password'),

    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
