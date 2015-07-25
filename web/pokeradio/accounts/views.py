from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView

from pokeradio.models import Profile

from .pipeline import get_or_create_user_profile

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))


class ProfileEdit(UpdateView):
    model = Profile
    template_name = 'accounts/edit_profile.html'
    fields = ['image', ]

    def get_object(self, *args, **kwargs):
        return get_or_create_user_profile(self.request.user)

    def get_success_url(self):
        return reverse('home')


edit_profile = ProfileEdit.as_view()
