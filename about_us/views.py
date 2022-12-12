from django.shortcuts import render
from .forms import *
from django.http import HttpResponse
from .models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime

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

def show_feedback_by_id(request, id):
    context = {
        'data': Feedback.objects.get(pk=id)
    }
    
    return render(request, 'show_feedback.html', context)

@csrf_exempt
def add_feedback_flutter(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        your_feedback = request.POST.get('your_feedback')
        new_feedback = Feedback(name=name, your_feedback=your_feedback, date=datetime.datetime().now())
        new_feedback.save()
        return HttpResponse(status=202)
