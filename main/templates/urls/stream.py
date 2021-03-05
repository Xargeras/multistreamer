from django.urls import path, include
from django.contrib.auth.decorators import login_required
from main import views


class Stream:
    paths = [path('stream/', include([
                path('', login_required(views.Broadcast.as_view()), name='stream'),
                path('create', login_required(views.CreateBroadcast.as_view()), name='stream_create'),
                path('<int:pk>/update', login_required(views.UpdateBroadcast.as_view()), name='stream_update'),
                path('<int:pk>/delete', login_required(views.DeleteBroadcast.as_view()), name='stream_delete'),
                path('my_list', login_required(views.ListBroadcast.as_view()), name='list_stream'),
                path('<int:pk>/update_key', login_required(views.UpdateInputKey.as_view()), name='update_input_key'),
            ]))]

    def get_url_list(self):
        return self.paths
