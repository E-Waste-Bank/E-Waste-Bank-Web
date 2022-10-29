from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from tips_and_tricks.models import TipsAndTrick
from tips_and_tricks.forms import AddForm

# Custom function to check the request type 
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def index(request):
    if 'q' in request.GET:
        q = request.GET['q']
        articles = TipsAndTrick.objects.filter(title__icontains=q).order_by('id')
        if q == '':
            paginator = Paginator(articles, 3)
            articles = paginator.get_page(q)
    else:
        articles = TipsAndTrick.objects.all().order_by('id')

    if is_ajax(request):
        html = render_to_string(
            template_name="tips_and_tricks/load_article.html", context={"articles": articles}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')
    posts_obj = paginator.get_page(page_number)
    response = {'articles': posts_obj, 'all_articles': articles}
    return render(request, 'tips_and_tricks/main.html', response)

# Function untuk add new article tips and tricks
def add(request):
    form = AddForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("/tips-and-tricks")

    # form = AddForm()
    # if request.method == "POST":
    #     form = AddForm(request.POST)

    #     if form.is_valid():
    #         title = form.cleaned_data['title']
    #         source = form.cleaned_data['source']
    #         pubDate = form.cleaned_data['published_date']
    #         imageURL = form.cleaned_data['imageURL']
    #         articleURL = form.cleaned_data['articleURL']
    #         briefDesc = form.cleaned_data['briefDesc']

    #         new_form = TipsAndTrick.objects.create(title=title, source=source, pubDate=pubDate, imageURL=imageURL, articleURL=articleURL, briefDes=briefDesc)
    #         new_form.save()

    #         result = {
    #             'fields':{
    #                 'title':new_form.title,
    #                 'source':new_form.source,
    #                 'pubDate':new_form.pubDate,
    #                 'imageURL':new_form.user.imageURL,
    #                 'articleURL':new_form.user.articleURL,
    #                 'briefDesc':new_form.user.briefDesc,
    #             },
    #             'pk':new_form.pk
    #         }
    #         return JsonResponse(result)
    response = {'form': form}
    return render(request, 'tips_and_tricks/add.html', response)

# Function untuk menampilkan load more articles
def load_more(request):
    offset = int(request.GET['offset'])
    limit = 3
    posts = TipsAndTrick.objects.all()[offset:limit + offset]
    totalData = TipsAndTrick.objects.count()
    data = {}
    posts_json = serializers.serialize('json', posts)
    return JsonResponse(data={
        'posts': posts_json,
        'totalResult': totalData
    })

# Function search_json
def search_json(request):
    if 'q' in request.GET:
        q = request.GET['q']
        articles = TipsAndTrick.objects.filter(title__icontains=q).order_by('id')
    else:
        articles = TipsAndTrick.objects.all().order_by('id')
    data = serializers.serialize('json', articles)
    return HttpResponse(data, content_type="application/json")