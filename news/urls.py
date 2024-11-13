from django.urls import path

from .views import PostList, PostDetail, PostFil, PostCreateNE, PostUpdate, PostDelete, MyPosts


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostFil.as_view(), name='post_filter'),
    path('create/', PostCreateNE.as_view(), name='post_create_ne'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update_ne'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete_ne'),
    path('myposts/', MyPosts.as_view(), name='my_posts'),
]
