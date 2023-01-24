from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend

User = get_user_model()


class EmailAuthBackend(DjangoModelBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):

        if email is None or password is None:
            return
        try:
            user = User._default_manager.get(email=email)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and \
                    self.user_can_authenticate(user):
                return user


class PhoneAuthBackend(DjangoModelBackend):

    def authenticate(self, request, username=None, phone=None, password=None,
                     **kwargs):
        if phone is None or password is None:
            return
        try:
            user = User._default_manager.get(phone=phone)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and \
                    self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        can = super().user_can_authenticate(user)
        return can and user.phone_is_valid