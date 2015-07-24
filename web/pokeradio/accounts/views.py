from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))
