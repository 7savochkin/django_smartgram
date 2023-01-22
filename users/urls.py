from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import SignInView, SignUpView

urlpatterns = [
    path('sign_in/', SignInView.as_view(), name='sign_in'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
]