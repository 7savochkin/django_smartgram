from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import SignInView, SignUpView, UserDetail

urlpatterns = [
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('profile/logout/', LogoutView.as_view(), name='logout'),
    path('profile/<username>/', UserDetail.as_view(), name='profile')
]