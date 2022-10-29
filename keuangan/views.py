from django.shortcuts import render
from keuangan.models import KeuanganAdmin, Cashout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers

# Create your views here.
def show_admin(request):
    keuangan_admin = KeuanganAdmin.objects.all().order_by()

    context = {
        'keuangan_admin': keuangan_admin,
    }

    return render(request, "admin.html", context)

def show_json(request):
    data = KeuanganAdmin.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url="")
def admin_update_cash(request):
    if request.METHOD == "POST":
        uang_user = request.POST.get('uang_user')

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()