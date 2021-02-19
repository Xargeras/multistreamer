from builtins import object

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password
from main.models import OutputBroadcast, InputBroadcast
from django.views.generic.edit import CreateView
from django.db import models
from django.urls import reverse
from main.forms import BroadcastSettings

import random
import string


# Create your views here.
def index_page(request):
    context = {
        'pagename': 'Главная',
    }
    return render(request, 'pages/index.html', context)


class CreateKey(CreateView):
    template_name = 'pages/curp.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    fields = ['name', 'url', 'key']

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return redirect('stream')


# Для получения ключа куда стримить
class BroadcastKey(View):
    context = {
        'pagename': 'Ключ',
    }
    dele = update = create = copy = False

    def get(self, request):
        if self.create:
            self.create_key(request)
        elif self.dele:
            self.delete_key(request)
        elif self.update:
            self.update_key(request)
        elif self.copy:
            self.copy_key()
        return redirect('stream')
        # return render(request, 'pages/curp.html', self.context)

    def create_key(self, request):
        broadcast = InputBroadcast.objects.filter(author=request.user)
        if not broadcast:
            broadcast = InputBroadcast()
            key = make_password(get_random_string())
            print(key)
            broadcast.author = request.user
            broadcast.key = key
            broadcast.save()

    def delete_key(self, request):
        broadcast = InputBroadcast.objects.filter(author=request.user)
        broadcast.delete()

    def update_key(self, requset):
        self.delete_key(requset)
        self.create_key(requset)

    def copy_key(self):
        pass


def get_random_string():
    str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
    return str
