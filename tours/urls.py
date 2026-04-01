from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tours/create/', views.create_tour, name='create_tour'),
    path('tours/<int:tour_id>/edit/', views.edit_tour, name='edit_tour'),
    path('tours/<int:tour_id>/delete/', views.delete_tour, name='delete_tour'),
    path('tours/<int:tour_id>/review/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/respond/', views.respond_to_review, name='respond_to_review'),
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('bookings/', views.manage_bookings, name='manage_bookings'),
    path('bookings/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/<int:user_id>/', views.send_message, name='send_message'),
]
