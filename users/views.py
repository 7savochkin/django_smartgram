from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.views.generic import FormView

from smartgram.mixins.views_mixins import UsernameDetailMixin
from users.forms import CustomAuthenticationForm, CustomUserCreationForm


User = get_user_model()


class UserDetail(LoginRequiredMixin, UsernameDetailMixin):
    model = User
    template_name = 'profile/profile_detail.html'


class SignInView(AuthLoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/sign_in.html'

    def form_valid(self, form):
        return super(SignInView, self).form_valid(form)

    def form_invalid(self, form):
        return super(SignInView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(SignInView, self).get_context_data(**kwargs)
        context.update({'title': 'Sign In'})
        return context


class SignUpView(FormView):
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('home')
    form_class = CustomUserCreationForm

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context.update({'title': 'Sign Up'})
        return context

    def form_valid(self, form):
        user = form.save(commit=True)
        self.request.session['user_id'] = user.id
        return super().form_valid(form)
