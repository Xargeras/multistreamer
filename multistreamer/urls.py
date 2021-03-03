"""multistreamer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView
from django_registration.backends.one_step.views import RegistrationView

from main import views
from multistreamer import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.StreamingTest.as_view(), name='test'),
    path('', views.index_page, name='index'),
    path('profile/<int:id>', views.profile_page, name='profile'),
    path('profile/setting', views.ProfileSettingView.as_view(), name='profilesetting'),
    path('', views.IndexPage.as_view(), name='index'),
    path('setting', views.ProfileSettingView.as_view(), name='setting'),
    path('stream/', login_required(views.StreamSettingView.as_view()), name='stream'),
    path('stream/create', login_required(views.CreateBroadcastOutputKey.as_view()), name='stream_create'),
    path('stream/update/<pk>', login_required(views.UpdateBroadcastOutputKey.as_view()), name='stream_update'),
    path('stream/delete/<pk>', login_required(views.DeleteBroadcastOutputKey.as_view()), name='stream_delete'),
    path('stream/create_key', login_required(views.BroadcastKey.as_view(create=True)), name='create_key'),
    path('stream/delete_key', views.BroadcastKey.as_view(dele=True), name='delete_key'),
    path('stream/update_key', views.BroadcastKey.as_view(update=True), name='update_key'),
    path('stream/copy_key', views.BroadcastKey.as_view(copy=True), name='copy_key'),
]

login_urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'menu': views.get_menu_context(),
                'pagename': 'Авторизация'
            }
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        "register/",
        RegistrationView.as_view(
            extra_context={
                'menu': views.get_menu_context(),
                'pagename': 'Регистрация'
            }
        ),
        name="django_registration_register",
    ),
    path(
        "register/closed/",
        TemplateView.as_view(
            template_name="django_registration/registration_closed.html",
            extra_context={
                'menu': views.get_menu_context(),
                'pagename': 'Регистрация'
            }
        ),
        name="django_registration_disallowed",
    ),
    path(
        "register/complete/",
        TemplateView.as_view(
            template_name="django_registration/registration_complete.html",
            extra_context={
                'menu': views.get_menu_context(),
                'pagename': 'Регистрация'
            }
        ),
        name="django_registration_complete",
    ),
]

urlpatterns += login_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
