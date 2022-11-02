from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from keuangan.models import KeuanganAdmin
from django.http import HttpResponseRedirect

# Create your views here.
def landing_page(request):
    return HttpResponseRedirect(reverse("about_us:show_about_us"))

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # redirect implementation https://stackoverflow.com/a/44807947
            next_url = request.GET.get('next')

            # redirect URL validation https://stackoverflow.com/a/60372947
            if next_url and url_has_allowed_host_and_scheme(next_url, None):
                next_url = iri_to_uri(next_url)
                response = redirect(next_url)

            else:
                # default is landing page
                response = redirect(reverse('home:landing_page'))

            return response
            
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect(reverse('home:login_user'))

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_keuangan = KeuanganAdmin.objects.create(
                user=new_user,
                uang_user=0
            )
            new_keuangan.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect(reverse('home:login_user'))
    
    context = {'form':form}
    return render(request, 'register.html', context)