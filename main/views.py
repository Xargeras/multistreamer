import random
import string

from django.contrib.auth.hashers import make_password
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse

from main.forms import UserSettings, AvatarSettings, PasswordSettings, BroadcastSettings
from main.models import Avatar, OutputBroadcast, InputBroadcast
from scripts.run import Server


def get_menu_context():
    return [
        {'url_name': 'votelist', 'name': 'Список голосований'},
    ]


class StreamingTest(View):
    internal_url = 'mystream'
    key = '95hb-4hcj-5fpa-1063-4ws6'
    server = Server()

    def get_context(self, request):
        return {
            'menu': get_menu_context(),
            'pagename': 'Тестовая трансляция',
            'server_online': self.server.is_server_online(),
            'url': f'{self.server.url}/{self.internal_url}',
        }

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'pages/streaming_test.html', self.get_context(request))

    @method_decorator(login_required)
    def post(self, request):
        if not self.server.is_server_online():
            self.server.start_server()
            self.server.start_broadcast(self.internal_url, self.key)
        else:
            self.server.stop_server()
            self.server.stop_broadcast()
        return redirect(reverse('test'))


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)


def profile_page(request, id):
    context = {
        'pagename': "Профиль",
        'menu': get_menu_context(),
        'user': get_object_or_404(User, id=id),
    }
    return render(request, 'pages/profile/profile.html', context)


class ProfileSettingView(View):
    context = {
        'pagename': "Настроки профиля",
        'menu': get_menu_context(),
    }

    @method_decorator(login_required)
    def get(self, request):
        self.context['name'] = request.user
        self.context['form'] = UserSettings(instance=request.user)
        self.context['avatar_form'] = AvatarSettings()
        self.context['change_password'] = PasswordSettings()
        avatar = Avatar.objects.filter(user=request.user)
        if avatar:
            self.context['user_avatar'] = avatar[0].image
        return render(request, 'pages/profile/profilesettings.html', self.context)

    @method_decorator(login_required)
    def post(self, request):
        if request.POST.get('avatar_form', None):
            avatar = Avatar.objects.filter(user=request.user)
            if not avatar:
                avatar = Avatar(user=request.user)
            else:
                avatar = avatar[0]
            form = AvatarSettings(request.POST, request.FILES, instance=avatar)
            if form.is_valid():
                form.save()
        elif request.POST.get('change_password', None):
            form = PasswordSettings(request.POST, instance=request.user)
            if form.is_valid():
                password = request.POST.get('password')
                new_password = request.POST.get('new_password', None)
                if new_password == password:
                    request.user.set_password(password)
                    request.user.save()
        else:
            form = UserSettings(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
        return redirect(reverse('profile', kwargs={"id": request.user.id}))


class IndexPage(View):
    context = {
        'pagename': 'Главная',
    }

    def get(self, request):
        return render(request, 'pages/stream/index.html', self.context)


class StreamStorageView(View):
    context = {
        'pagename': 'Записи стримов',
    }

    def get(self, request):
        return render(request, 'pages/stream/storage.html', self.context)


class StreamSettingView(View):
    context = {
        'pagename': 'Настройка стрима',
    }

    def get(self, request):
        places = OutputBroadcast.objects.filter(author=request.user)
        self.context['places'] = places
        return render(request, 'pages/curp.html', self.context)


class CreateBroadcastOutputKey(CreateView):
    template_name = 'pages/curp.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    fields = ['name', 'url', 'key']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.input_key = InputBroadcast.objects.filter(author=self.request.user)
        self.object.author = self.request.user
        self.object.input = self.input_key[0]
        self.object.save()
        return redirect('stream')


class UpdateBroadcastOutputKey(UpdateView):
    template_name = 'pages/curp.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    fields = ['name', 'url', 'key']
    success_url = '/stream/'


class DeleteBroadcastOutputKey(DeleteView):
    template_name = 'pages/curp.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    success_url = '/stream/'


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
