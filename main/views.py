from django.shortcuts import render

# Create your views here.
def index_page(request):
    context = {
        'pagename': 'Главная',
    }
    return render(request, 'pages/index.html', context)
