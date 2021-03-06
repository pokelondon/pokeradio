from django.contrib.auth import logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    context = {
        'logout': True,
    }
    return render(request, 'login.html', context)
