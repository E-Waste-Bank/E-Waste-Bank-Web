from django.shortcuts import render, redirect
from keuangan.models import KeuanganAdmin, Cashout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.urls import reverse
from django.core import serializers
from .forms import *
from .decorators import admin_only


# Create your views here.
@login_required(login_url="/login/")
def show_keuangan(request: HttpRequest):
    if request.user.groups.exists():
        groups = request.user.groups.all()

        for group in groups:
            if group.name == "admin":
                return HttpResponseRedirect(reverse("keuangan:show_admin"))

    return HttpResponseRedirect(reverse("keuangan:show_user"))

@login_required(login_url="/login/")
@admin_only
def show_admin(request: HttpRequest):
    context = {
        'admin_cashout_form': EditCashoutForm(),
        'admin_uang_user_form': EditUangUserForm()
    }
    return render(request, "admin.html", context)

@login_required(login_url="/login/")
def show_user(request: HttpRequest):
    context = {
        'cashout_form': CreateCashoutForm()
    }
    return render(request, "user.html", context)

@login_required(login_url="/login/")
def user_get_keuangan_data_json(request: HttpRequest):
    return HttpResponse(serializers.serialize("json", KeuanganAdmin.objects.filter(user = request.user)), content_type="application/json")

@login_required(login_url="/login/")
def user_get_all_cashouts_json(request: HttpRequest): # TODO test
    return HttpResponse(serializers.serialize("json", Cashout.objects.filter(user = request.user)), content_type="application/json")

@login_required(login_url="/login/") # TODO set login URL, create tests
def user_create_cashout(request: HttpRequest):
    if request.method == "POST":
        form = CreateCashoutForm(request.POST)
        if form.is_valid():
            # validasi kecukupan uang
            uang_model_user = KeuanganAdmin.objects.get(user = request.user)
            jumlah_uang_user = uang_model_user.uang_user
            jumlah_uang_ditarik = form.cleaned_data['amount']

            if jumlah_uang_ditarik <= 0:
                return JsonResponse({"status": "Invalid amount"}, status=400)

            if jumlah_uang_user < jumlah_uang_ditarik:
                return JsonResponse({"status": "Not enough funds"}, status=400)

            new_cashout = Cashout.objects.create(
                user = request.user,
                uang_model = uang_model_user,
                amount = jumlah_uang_ditarik,
            )

            new_cashout.save()

            uang_model_user.uang_user -= jumlah_uang_ditarik
            uang_model_user.save()

            return HttpResponse(serializers.serialize("json", [new_cashout]), content_type="application/json")
    
        else:
            # input tdk sesuai validasi pada forms.py
            return JsonResponse({"status": "Invalid input"}, status=400)
            
    else:
        # hanya boleh POST ke endpoint ini
        response = JsonResponse({"status": "Invalid method"}, status=405)

        # Allow header as per HTTP spec https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405
        response['Allow'] = 'POST'
        return response

@login_required(login_url="/login/")
def user_get_cashout_html(request: HttpRequest, id: int):
    if Cashout.objects.filter(pk = id).exists():
        cashout_object = Cashout.objects.get(pk = id)
        # validasi user adlh admin ATAU user pemilik cashout
        authorized = False

        if request.user == cashout_object.user:
            authorized = True

        if not authorized and request.user.groups.exists():
            groups = request.user.groups.all()

            for group in groups:
                if group.name == "admin":
                    authorized = True

        context = {
            "cashout_object": cashout_object
        }
        if authorized:
            return render(request, "cashout.html", context)
        
        else:
            return HttpResponse("Anda tidak diperbolehkan mengakses halaman ini. <br> You are forbidden from accessing this page.", status=403)

    # jika obj cashout dgn id tsb tdk ditemukan
    return HttpResponse(f"ID: {id} <br> Penarikan tidak ditemukan. <br> Cashout not found.", status=404)

@login_required(login_url="/login/")
@admin_only
def admin_get_keuangan_data_json(request: HttpRequest):
    return HttpResponse(serializers.serialize("json", KeuanganAdmin.objects.all(), use_natural_foreign_keys=True), content_type="application/json")

@login_required(login_url="/login/")
@admin_only
def admin_get_all_cashouts_json(request: HttpRequest):
    return HttpResponse(serializers.serialize("json", Cashout.objects.all(), use_natural_foreign_keys=True), content_type="application/json")

@login_required(login_url="/login/")
@admin_only
def admin_edit_cashout(request: HttpRequest, id: int):
    if request.method == "POST":
        form = EditCashoutForm(request.POST)

        if form.is_valid():
            cashout_object = Cashout.objects.get(pk = id)
            cashout_object.approved = form.cleaned_data['approved']
            cashout_object.save()
    
    return redirect('keuangan:show_admin')

@login_required(login_url="/login/")
@admin_only
def admin_edit_uang_user(request: HttpRequest, id: int):
    if request.method == "POST":
        form = EditUangUserForm(request.POST)

        if form.is_valid():
            user = KeuanganAdmin.objects.get(pk = id)
            uang_tambahan = form.cleaned_data['uang_user']
            user.uang_user += uang_tambahan
            user.save()
        
    return redirect('keuangan:show_admin')
