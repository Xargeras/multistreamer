import json
import string
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from main.forms import (UserSettings, AvatarSettings, PasswordSettings,
                        BroadcastSettings, InputBroadcastSettings)
from main.forms import YoutubeBroadcastSettings
from main.models import Avatar, OutputBroadcast, InputBroadcast
from main.models import YoutubeSettings
from scripts.run import Server
from scripts.youtube import get_user_credentials, stream


def get_menu_context():
    return [
        {'url_name': 'votelist', 'name': 'Список голосований'},
    ]


def profile_page(request, id):
    context = {
        'pagename': 'Профиль',
        'menu': get_menu_context(),
        'user': get_object_or_404(User, id=id),
    }
    return render(request, 'pages/profile/profile.html', context)


class ProfileSettingView(View):
    context = {
        'pagename': 'Настроки профиля',
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
        return redirect(reverse('setting'))


class IndexPage(View):
    context = {
        'pagename': 'Главная',
    }

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('list_stream'))
        else:
            return render(request, 'pages/index.html', self.context)


class StreamStorageView(View):
    context = {
        'pagename': 'Записи стримов',
    }

    def get(self, request):
        return render(request, 'pages/stream/storage.html', self.context)


class StartBroadcast(View):
    context = {
        'pagename': 'Запуск',
    }

    def get(self, request, id):
        return redirect(reverse('stream_detail', kwargs={'id': id}))

    def post(self, request, id):
        server = Server.get_instance()
        broadcast = get_object_or_404(InputBroadcast, id=id, author=request.user)
        outputs = OutputBroadcast.objects.filter(input_broadcast=broadcast, is_active=True)
        youtubes = YoutubeSettings.objects.filter(input_broadcast=broadcast, is_active=True)
        outputs = list(chain(youtubes, outputs))
        if server.is_broadcast_online_list(outputs):
            server.stop_broadcast_list(outputs)
        else:
            for youtube in youtubes:
                settings = {
                    "title": youtube.title,
                    "description": "Restream via MultiStream https://multistream.io " + youtube.description,
                    "resolution": youtube.choices[youtube.resolution][1],
                    "privacy": youtube.privacy_choices[youtube.privacy][1]
                }
                youtube.key = stream(youtube.user_credentials, settings)
                youtube.save()
            server.start_broadcast_list(outputs, broadcast.key, broadcast.type)
        return redirect(reverse('stream_detail', kwargs={'id': id}))


class ListBroadcast(ListView):
    template_name = 'pages/stream/list.html'
    model = InputBroadcast

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Список моих трансляций'
        return context


class DetailBroadcast(DetailView):
    template_name = 'pages/stream/detail.html'
    model = InputBroadcast
    pk_url_kwarg = 'id'
    extra_context = {'pagename': 'Просмотр параметров трансляции'}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['server_url'] = Server.get_instance().get_url(self.object.type) + '/'
        context['youtube'] = YoutubeSettings.objects.filter(input_broadcast=self.object)
        context['outputs'] = list(chain(OutputBroadcast.objects.filter(input_broadcast=self.object), context['youtube']))
        context['is_online'] = Server.get_instance().is_broadcast_online_list(context['outputs'])
        return context


class CreateBroadcast(CreateView):
    template_name = 'pages/stream/create.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    fields = ['name', 'url', 'key', 'bitrate']
    extra_context = {'pagename': 'Создание Трансляции'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.input_broadcast_id = self.kwargs['id']
        self.object.save()
        return redirect('stream_detail', self.kwargs['id'])


class CreateYoutubeBroadcast(CreateView):
    template_name = 'pages/stream/create.html'
    model = YoutubeSettings
    model_form = YoutubeBroadcastSettings
    fields = ['name', 'title', 'description', 'resolution', 'privacy']
    extra_context = {'pagename': 'Создание Трансляции'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # settings = {
        #     "title": self.object.title,
        #     "description": "Restream via MultiStream https://multistream.io " + self.object.description,
        #     "resolution": self.object.choices[self.object.resolution][1],
        #     "privacy": self.object.privacy_choices[self.object.privacy][1]
        # }
        self.object.author = self.request.user
        # if YoutubeSettings.objects.filter(author=self.object.author):
        #     user = YoutubeSettings.objects.filter(author=self.object.author)
        #     token = user[0].user_credentials
        # else:
        #     token = get_user_credentials()
        token = get_user_credentials()
        self.object.user_credentials = json.loads(token)
        print(type(json.loads(token)))
        self.object.input_broadcast_id = self.kwargs['id']
        self.object.save()
        return redirect('stream_detail', self.kwargs['id'])


class UpdateYoutubeBroadcast(UpdateView):
    template_name = 'pages/stream/update.html'
    model = YoutubeSettings
    model_form = YoutubeBroadcastSettings
    pk_url_kwarg = 'out_id'
    fields = ['name', 'title', 'description', 'resolution', 'privacy']
    extra_context = {'pagename': 'Обновление трансляции'}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.input_broadcast_id = self.kwargs['id']
        self.object.save()
        return redirect('stream_detail', self.kwargs['id'])


class UpdateBroadcast(UpdateView):
    template_name = 'pages/stream/update.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    pk_url_kwarg = 'out_id'
    fields = ['name', 'url', 'key', 'bitrate']
    extra_context = {'pagename': 'Обновление трансляции'}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.input_broadcast_id = self.kwargs['id']
        self.object.save()
        return redirect('stream_detail', self.kwargs['id'])


class DeleteBroadcast(DeleteView):
    template_name = 'pages/stream/delete.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    pk_url_kwarg = 'out_id'
    success_url = '/stream/'
    extra_context = {'pagename': 'Удаление трансляции'}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('stream_detail', kwargs['id'])


class ChangeState(View):
    context = {
        'pagename': 'Смена статуса',
    }
    is_youtube = False

    def get(self, request, id):
        out_id = request.GET.get('out_id', -1)
        if self.is_youtube:
            output = get_object_or_404(YoutubeSettings, id=out_id)
        else:
            output = get_object_or_404(OutputBroadcast, id=out_id)
        output.is_active = not output.is_active
        output.save()
        return redirect(reverse('stream_detail', kwargs={'id': id}))


class CreateInputKey(CreateView):
    template_name = 'pages/stream/create_input_key.html'
    model = InputBroadcast
    model_form = InputBroadcastSettings
    fields = ['name', 'type']
    extra_context = {'pagename': 'Создание ключа'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        input_key = get_random_string(length=20, allowed_chars=string.ascii_letters + string.digits)
        self.object.key = input_key
        self.object.author = self.request.user
        self.object.save()
        return redirect('list_stream')


class UpdateInputKey(UpdateView):
    template_name = 'pages/stream/create_input_key.html'
    model = InputBroadcast
    model_form = InputBroadcastSettings
    fields = ['name', 'type']
    extra_context = {'pagename': 'Изменение входящей трансляции'}
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return redirect('stream_detail', self.object.id)


class DeleteInputBroadcast(DeleteView):
    template_name = 'pages/stream/delete.html'
    model = InputBroadcast
    model_form = BroadcastSettings
    pk_url_kwarg = 'id'
    success_url = '/stream/'
    extra_context = {'pagename': 'Удаление трансляции'}

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)
