from django.contrib import admin
from django.urls import path
from . import views

app_name = 'twitter'
urlpatterns = [
    path('top/', views.top, name='top'),
    path('tweet/', views.tweet, name='tweet'),
    path('tweet_input/', views.TweetInputView.as_view(), name='tweet_input'),
    path('user_list/', views.UserListView.as_view(), name='user_list'),
    path('other_user/<int:other_user_id>/', views.other_user, name='other_user'),
    path('followed/<int:other_user_id>/', views.user_followed, name='followed'),
    path('follow_deleted/<int:other_user_id>/', views.follow_deleted, name='follow_deleted'),
    path('favorite_list/', views.favorite_list, name='favorite_list'),
    path('add_favorite/<int:favorite_tweet_id>/', views.add_favorite, name='add_favorite'),
    path('del_favorite/<int:favorite_tweet_id>/', views.del_favorite, name='del_favorite'),
]
