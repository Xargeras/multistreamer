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

from main import views
from main.templates.urls.stream import Stream
from main.templates.urls.login import Login
from multistreamer import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/<int:id>/', views.profile_page, name='profile'),
    path('profile/setting/', views.ProfileSettingView.as_view(), name='profilesetting'),
    path('test/', views.StreamingTest.as_view(), name='test'),
    path('', views.IndexPage.as_view(), name='index'),
    path('setting/', views.ProfileSettingView.as_view(), name='setting'),
]

urlpatterns += Stream().get_url_list()
urlpatterns += Login().get_url_list()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
