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
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django_registration.backends.one_step.views import RegistrationView
from main import views
from multistreamer import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('profile/<int:id>', views.profile_page, name='profile'),
    path('profile/setting', views.ProfileSettingView.as_view(), name='profilesetting'),

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
