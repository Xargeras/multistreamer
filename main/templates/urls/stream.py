from django.urls import path, include
from django.contrib.auth.decorators import login_required
from main import views


class Stream:
    paths = [path('stream/', include([
                path('create', login_required(views.CreateBroadcast.as_view()), name='stream_create'),
                path('<id>/update', login_required(views.UpdateBroadcast.as_view()), name='stream_update'),
                path('<id>/delete', login_required(views.DeleteBroadcast.as_view()), name='stream_delete'),
                path('<id>/detail', login_required(views.DetailBroadcast.as_view()), name='stream_detail'),
                path('my_list', login_required(views.ListBroadcast.as_view()), name='list_stream'),
                path('<id>/update_key', login_required(views.UpdateInputKey.as_view()), name='update_input_key'),
            ]))]

    def get_url_list(self):
        return self.paths
