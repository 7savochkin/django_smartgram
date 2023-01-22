from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import \
    UserCreationForm, UsernameField

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
        "username", "email", "phone", "first_name", "last_name"
        )
        field_classes = {
            'username': UsernameField,
            'email': forms.EmailField,
        }

        def clean(self):
            self.instance.is_active = False
            return self.cleaned_data


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput())
    phone = forms.CharField(max_length=30, required=False)

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_sign_in': _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        try:
            email = self.cleaned_data['email']
            phone = self.cleaned_data['phone']
            password = self.cleaned_data['password']
        except KeyError:
            raise ValidationError('Fields are required')
        if not email and not phone:
            raise ValidationError('Email or phone number is required')
        if password:
            kwargs = {'password': password, 'email': email}
            if phone and not email:
                kwargs.pop('email')
                kwargs.update({'phone': phone})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_sign_in'],
            code='invalid_sign_in')
