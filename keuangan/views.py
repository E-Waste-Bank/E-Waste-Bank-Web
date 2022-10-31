from django.shortcuts import render
from keuangan.models import KeuanganAdmin, Cashout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.urls import reverse
from django.core import serializers
from .forms import *



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
def show_admin(request: HttpRequest):
    context = {
        'form': EditCashoutForm()
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
        return JsonResponse({"status": "Invalid method"}, status=405)

# ! INITIAL NOT DONE !
@login_required(login_url="/login/")
def user_get_cashout_html(request: HttpRequest, id: int):
    if Cashout.objects.filter(pk = id).exists():
        cashout_object = Cashout.objects.get(pk = id)
        # validasi user adlh admin ATAU user pemilik cashout
        authorized = False

        if request.user.groups.exists():
            groups = request.user.groups.all()

            for group in groups:
                if group.name == "admin":
                    authorized = True

        if request.user == cashout_object.user:
            authorized = True

        context = {
            "cashout_object": cashout_object
        }
        if authorized:
            return render(request, "cashout.html", context)
        
        else:
            return HttpResponse(status=403)

    # jika obj cashout dgn id tsb tdk ditemukan
    return HttpResponse(status=404)

@login_required(login_url="/login/")
def admin_get_keuangan_data_json(request: HttpRequest):
    return HttpResponse(serializers.serialize("json", KeuanganAdmin.objects.all()), content_type="application/json")

@login_required(login_url="/login/")
def admin_get_all_cashouts_json(request: HttpRequest):
    return HttpResponse(serializers.serialize("json", Cashout.objects.all()), content_type="application/json")

@login_required(login_url="/login/")
def admin_edit_cashout(request: HttpRequest, id: int): # TODO: Still can't get the checkbox value
    if request.method == "POST":
        form = EditCashoutForm(request.POST)
        if form.is_valid():
            cashout_object = Cashout.objects.get(pk = id)

            cashout_object.approved = request.POST.get('approved') # form.cleaned_data['approved']

            cashout_object.save()
    
    return HttpResponseRedirect(reverse("keuangan:show_admin"))
