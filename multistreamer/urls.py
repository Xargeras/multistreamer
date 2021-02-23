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
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('stream/', views.StreamSettingView.as_view(), name='stream'),
    path('stream/create', login_required(views.CreateBroadcastOutputKey.as_view()), name='stream_create'),
    path('stream/update/<pk>', login_required(views.UpdateBroadcastOutputKey.as_view()), name='stream_update'),
    path('stream/delete/<pk>', login_required(views.DeleteBroadcastOutputKey.as_view()), name='stream_delete'),
    path('stream/create_key', login_required(views.BroadcastKey.as_view(create=True)), name='create_key'),
    path('stream/delete_key', views.BroadcastKey.as_view(dele=True), name='delete_key'),
    path('stream/update_key', views.BroadcastKey.as_view(update=True), name='update_key'),
    path('stream/copy_key', views.BroadcastKey.as_view(copy=True), name='copy_key'),
]
