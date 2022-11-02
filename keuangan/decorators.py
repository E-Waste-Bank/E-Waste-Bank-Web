from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'admin':
			return view_func(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse("keuangan:show_user"))

	return wrapper_function