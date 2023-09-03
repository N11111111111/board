from django.urls import path, include
from .views import *
from .views import subscription
from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

from . import views

urlpatterns = [
    path('', cache_page(10)(PostList.as_view())),
    path('news/', PostList.as_view(), name='posts'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('subscription/', subscription, name='subscription'),
    path('search/', SearchPosts.as_view(), name='post_search'),
    path('news/add/', PostCreateView.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('responds/<int:pk>', responds, name='respond_create'),
    path('responses/', ResponceListView.as_view(), name='respond_list'),






]









