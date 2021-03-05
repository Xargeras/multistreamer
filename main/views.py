import string

from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse

from main.forms import UserSettings, AvatarSettings, PasswordSettings, BroadcastSettings
from main.models import Avatar, OutputBroadcast


def get_menu_context():
    return [
        {'url_name': 'votelist', 'name': 'Список голосований'},
    ]


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
        return render(request, 'pages/index.html', self.context)


class ListBroadcast(ListView):
    template_name = 'pages/stream/list.html'
    model = OutputBroadcast

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Список моих трансляций'
        return context


class DetailBroadcast(DetailView):
    template_name = 'pages/stream/detail.html'
    model = OutputBroadcast


class CreateBroadcast(CreateView):
    template_name = 'pages/stream/create.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    fields = ['name', 'url', 'output_key']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.input_key = get_random_string(length=20, allowed_chars=string.ascii_letters + string.digits)
        self.object.save()
        return redirect('stream')


class UpdateBroadcast(UpdateView):
    template_name = 'pages/stream/update.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    fields = ['name', 'url', 'output_key']
    success_url = '/stream/detail/'


class DeleteBroadcast(DeleteView):
    template_name = 'pages/stream/delete.html'
    model = OutputBroadcast
    model_form = BroadcastSettings
    success_url = '/stream/my_list/'


class UpdateInputKey(View):
    context = {'pagename': 'Обновление ключа'}

    def get(self, request, pk):
        stream = get_object_or_404(OutputBroadcast, id=pk)
        input_key = get_random_string(length=20, allowed_chars=string.ascii_letters + string.digits)
        stream.input_key = input_key
        self.context['input_key'] = input_key
        stream.save()
        return render(request, 'pages/stream/update_key.html', self.context)


class Broadcast(View):
    context = {'pagename': 'Трансляция'}

    def get(self, request):
        return render(request, 'pages/stream/main.html', self.context)
