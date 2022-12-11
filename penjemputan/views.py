from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from penjemputan.forms import CreatePenjemputanForm
from penjemputan.models import Penjemputan
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.views.decorators.csrf import csrf_exempt
from penjemputan.decorators import admin_only
# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required(login_url='/login/')
def show_penjemputan(request):
    createForm = CreatePenjemputanForm(request.POST or None)
    if request.user.groups.exists():
        groups = request.user.groups.all()
        for group in groups:
            if group.name == "admin":
                penjemputan = Penjemputan.objects.all()
                role = 'admin'
                break 
    else:
        penjemputan = Penjemputan.objects.filter(user = request.user)
        role = 'user'
    context = {
        'penjemputan': penjemputan,
        'forms': createForm,
        'role': role
    }
    return render(request, 'penjemputan.html', context)

def show_json(request):
    if request.user.groups.exists():
        groups = request.user.groups.all()
        for group in groups:
            if group.name == "admin":
                data_penjemputan_json = Penjemputan.objects.all()
                break 
    else:
        data_penjemputan_json = Penjemputan.objects.filter(user = request.user)
    return HttpResponse(serializers.serialize("json", data_penjemputan_json), content_type="application/json")

@csrf_exempt
def add_penjemputan(request):
    if is_ajax(request) and request.method == 'POST':
        alamat = request.POST.get('alamat')
        tanggal_jemput = request.POST.get('tanggal_jemput')
        waktu_jemput = request.POST.get('waktu_jemput')
        jenis_sampah = request.POST.get('jenis_sampah')
        berat_sampah = request.POST.get('berat_sampah')
        new_penjemputan = Penjemputan(user=request.user, alamat=alamat, tanggal_jemput=tanggal_jemput, waktu_jemput=waktu_jemput, waktu_sekarang=datetime.datetime.now(), jenis_sampah=jenis_sampah, berat_sampah=berat_sampah, is_finished=False)
        new_penjemputan.save()
        return redirect('penjemputan:show_penjemputan')

@csrf_exempt
@admin_only
def delete_penjemputan(request, id):
    penjemputan = Penjemputan.objects.get(pk=id)
    penjemputan.delete()
    return redirect('penjemputan:show_penjemputan')

@csrf_exempt
@admin_only
def update_penjemputan(request, id):
    penjemputan = Penjemputan.objects.get(pk=id)
    if penjemputan.is_finished:
        penjemputan.is_finished = False
    else:
        penjemputan.is_finished = True
    penjemputan.save()
    return redirect('penjemputan:show_penjemputan')

