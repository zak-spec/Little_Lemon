from django.urls import path
from .views import (
    HomeView, AboutView, ReservationListView, BookView,
    MenuView, DisplayMenuItemView, BookingAPI
)


urlpatterns = [
    path('', HomeView.as_view, name="home"),
    path('about/', AboutView.as_view, name="about"),
    path('book/', BookView.as_view, name="book"),
    path('reservations/', ReservationListView.as_view, name="reservations"),
    path('menu/', MenuView.as_view, name="menu"),
    path('menu_item/<int:pk>/', DisplayMenuItemView.as_view, name="menu_item"),  
    path('bookings', BookingAPI.as_view, name='bookings'), 
]