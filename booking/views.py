from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from booking.models import Room


def main_page(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, template_name="bookingapp/index.html", context=context)


def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, template_name="bookingapp/room_list.html", context=context)
