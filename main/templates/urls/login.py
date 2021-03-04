from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django_registration.backends.one_step.views import RegistrationView
from main import views


class Login:
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

    def get_url_list(self):
        return self.login_urlpatterns
