from django.urls import path
from .views import PostCreateAR, PostUpdate, PostDelete


urlpatterns = [
    path('create/', PostCreateAR.as_view(), name='post_create_ar'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update_ar'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete_ar'),
]