from django.urls import path, include
from django.contrib.auth.decorators import login_required
from main import views


class Stream:
    paths = [path('stream/', include([
                path('/', login_required(views.StreamSettingView.as_view()), name='stream'),
                path('/create', login_required(views.CreateBroadcastOutputKey.as_view()), name='stream_create'),
                path('/update/<pk>', login_required(views.UpdateBroadcastOutputKey.as_view()), name='stream_update'),
                path('/delete/<pk>', login_required(views.DeleteBroadcastOutputKey.as_view()), name='stream_delete'),
                path('/create_key', login_required(views.CreateInputBroadcastKey.as_view()), name='create_key'),
                path('/<int:pk>/delete_key', login_required(views.DeleteInputBroadcastKey.as_view()), name='delete_key'),
                path('/<int:pk>/update_key', login_required(views.UpdateInputBroadcastKey.as_view()), name='update_key'),
                path('/list_keys', login_required(views.ListBroadcastKey.as_view()), name='list_keys'),
                path('/<int:pk>/detail_key', login_required(views.DetailInputBroadcastKey.as_view()), name='detail_key')
            ]))]

    def get_url_list(self):
        return self.paths
