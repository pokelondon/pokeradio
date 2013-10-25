from django.shortcuts import render

def login(request):
	if request.user.is_authenticated():
	    return request.redirect('home')
	return render(request,'login.html')
