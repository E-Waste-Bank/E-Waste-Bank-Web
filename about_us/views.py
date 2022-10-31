from django.shortcuts import render
from .forms import *
from django.http import HttpResponse
from .models import *
from django.core import serializers


# Create your views here.
def show_about_us(request):
    context = {
        'feedback_form': FeedbackForm()
    }
    return render(request, 'about_us.html', context)

def add_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            return HttpResponse(status=400)

def get_feedback_json(request):
    latest_three = Feedback.objects.all().order_by('-pk')[:3]
    return HttpResponse(serializers.serialize("json", latest_three), content_type="application/json")

# def show_json_by_id(request, id):
#     data = Feedback.objects.filter(pk=id)
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")
