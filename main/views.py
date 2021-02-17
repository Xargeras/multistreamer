from django.shortcuts import render
from django.views import View


class IndexPage(View):
    context = {
        'pagename': 'Главная',
    }

    def get(self, request):
        return render(request, 'pages/index.html', self.context)


class SettingProfileView(View):
    context = {
        'pagename': 'Настройки',
    }

    def get(self, request):
        return render(request, 'pages/account.html', self.context)


