from django.urls import path
from django.contrib.auth.decorators import login_required
from main import views


class Stream:
    paths = \
        [
            path('stream/', login_required(views.StreamSettingView.as_view()), name='stream'),
            path('stream/create', login_required(views.CreateBroadcastOutputKey.as_view()), name='stream_create'),
            path('stream/update/<pk>', login_required(views.UpdateBroadcastOutputKey.as_view()), name='stream_update'),
            path('stream/delete/<pk>', login_required(views.DeleteBroadcastOutputKey.as_view()), name='stream_delete'),
            path('stream/create_key', login_required(views.BroadcastKey.as_view(create=True)), name='create_key'),
            path('stream/delete_key', views.BroadcastKey.as_view(dele=True), name='delete_key'),
            path('stream/update_key', views.BroadcastKey.as_view(update=True), name='update_key'),
            path('stream/copy_key', views.BroadcastKey.as_view(copy=True), name='copy_key')
        ]

    def get_url_list(self):
        return self.paths
