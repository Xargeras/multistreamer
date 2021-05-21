from django.urls import path, include
from django.contrib.auth.decorators import login_required
from main import views


class Stream:
    paths = [path('stream/', include([
                path('storage/', login_required(views.StreamStorageView.as_view())),
                path('', login_required(views.ListBroadcast.as_view()), name='list_stream'),
                path('<int:id>/', login_required(views.DetailBroadcast.as_view()), name='stream_detail'),
                path('<int:id>/start/', login_required(views.StartBroadcast.as_view()), name='stream_start'),
                path('<int:id>/update', login_required(views.UpdateInputKey.as_view()), name='update_input_key'),
                path('<int:id>/delete', login_required(views.DeleteInputBroadcast.as_view()), name='delete_input_key'),
                path('create/', login_required(views.CreateInputKey.as_view()), name='create_input_key'),
                path('<int:id>/output/create/', login_required(views.CreateBroadcast.as_view()), name='stream_create'),
                path('<int:id>/output/create_youtube/', login_required(views.CreateYoutubeBroadcast.as_view()), name='youtube_create'),
                path('<int:id>/output/<int:out_id>/update_youtube/', login_required(views.UpdateYoutubeBroadcast.as_view()), name='youtube_update'),
                path('<int:id>/output/<int:out_id>/update/', login_required(views.UpdateBroadcast.as_view()), name='stream_update'),
                path('<int:id>/output/<int:out_id>/delete/', login_required(views.DeleteBroadcast.as_view()), name='stream_delete'),
                path('<int:id>/output/change/', login_required(views.ChangeState.as_view()), name='stream_change_state'),
            ]))]

    def get_url_list(self):
        return self.paths
