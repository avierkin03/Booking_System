from django.urls import path
from booking import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('rooms/', views.room_list, name='rooms'),
    #path('booking/', views.book_room, name='booking'),
]