from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('about/', views.about, name='about'),
    path('show/', views.event_show, name='event_show'),
    path('create/', views.event_create, name='event_create'),
    path('update/<int:pk>/', views.event_update, name='event_update'),
    path('comment_update/<int:pk>/', views.comment_update, name='comment_update'),
    path('delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('search_event/', views.search_event, name='search-event'),
    path('search_private_event/', views.search_private_event, name='search_private_event'),
    path('search_by_category/', views.search_by_category, name='search_by_category'),
    path('search_by_time_and_live/', views.search_by_time_and_live, name='search_by_time_and_live'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('comment/', views.comment_view, name='comment'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('heart_comment/<int:comment_id>/', views.heart_comment, name='heart_comment'),
    path('api/events/', views.search_place, name='search_place'),
    path('profile/register/', views.profile_register, name='profile_register'),
    path('profile_detail/', views.profile_detail, name='profile_detail'),
]

