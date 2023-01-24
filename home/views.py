from django.contrib.auth.views import LoginView as AuthLoginView

from posts.models import Post
from users.forms import CustomAuthenticationForm


class HomeView(AuthLoginView):
    form_class = CustomAuthenticationForm
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({'object_list': Post.objects.iterator()})
        return context
