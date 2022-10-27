from django.shortcuts import render
from keuangan.models import KeuanganAdmin, Cashout
from django.contrib.auth.decorators import login_required

# Create your views here.
def show_admin(request):
    keuangan_admin = KeuanganAdmin.objects.all()

    context = {
        'keuangan_admin': keuangan_admin,
    }

    return render(request, "admin.html", context)