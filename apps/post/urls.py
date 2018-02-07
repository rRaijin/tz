from django.conf.urls import url

from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, UserList, UserDetail

urlpatterns = [
    url(r'^(?P<id>\d+)/$', PostDetail.as_view(), name='detail'),
    url(r'^(?P<id>\d+)/update/$', PostUpdate.as_view(), name='update'),
    url(r'^(?P<id>\d+)/delete/$', PostDelete.as_view(), name='delete'),
    url(r'^create/', PostCreate.as_view(), name='create'),
    url(r'^users/(?P<id>\d+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^$', PostsList.as_view(), name='list'),
]