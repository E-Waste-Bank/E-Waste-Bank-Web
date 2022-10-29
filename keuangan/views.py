from django.shortcuts import render
from keuangan.models import KeuanganAdmin, Cashout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.core import serializers

# Create your views here.
@login_required
def show_keuangan(request: HttpRequest):
    if request.user.groups.exists():
        groups = request.user.groups.all()

        for group in groups:
            if group.name == "admin":
                return HttpResponseRedirect(reverse("keuangan:show_admin"))

    return HttpResponseRedirect(reverse("keuangan:show_user"))

def show_admin(request):
    keuangan_admin = KeuanganAdmin.objects.all()

    context = {
        'keuangan_admin': keuangan_admin,
    }

    return render(request, "admin.html", context)

@login_required
def show_user(request: HttpRequest): # test DONE
    data_keuangan = KeuanganAdmin.objects.get(user = request.user)

    context = {
        'data_keuangan': data_keuangan,
    }

    return render(request, "user.html", context)
