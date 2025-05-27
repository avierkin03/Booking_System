from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from booking.models import Room


# функція представення головної сторінки та пошуку кімнат
def main_page(request):
    rooms = Room.objects.all()  # За замовчуванням повертаємо всі номери
    context = {
        'rooms': rooms,
        'start_date': '',
        'end_date': '',
        'quantity': '',
        'price_from': '',
        'price_to': '',
        'filtered': False
    }

    if request.method == "POST":
        # Отримуємо дані з POST-запиту
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        quantity = request.POST.get('quantity')
        price_from = request.POST.get('price_from')
        price_to = request.POST.get('price_to')

        # Перевіряємо, чи є start_date і end_date
        if start_date and end_date:
            try:
                # Фільтруємо вільні номери
                rooms = Room.objects.exclude(bookings__start_time__lt=end_date,bookings__end_time__gt=start_date)
                # Додаємо додаткові фільтри, якщо вони вказані
                if quantity:
                    rooms = rooms.filter(capacity__gte=int(quantity))
                if price_from:
                    rooms = rooms.filter(price__gte=float(price_from))
                if price_to:
                    rooms = rooms.filter(price__lte=float(price_to))
            # Обробка помилки, якщо формат дати некоректний
            except ValueError:
                rooms = Room.objects.all()  # Повертаємо всі номери при помилці

        # Оновлюємо контекст із введеними даними
        context.update({
            'rooms': rooms,
            'start_date': start_date,
            'end_date': end_date,
            'quantity': quantity,
            'quantity': quantity,
            'price_from': price_from,
            'price_to': price_to,
            'filtered': True
        })

    return render(request, template_name="bookingapp/index.html", context=context)


# функція представення списку всіх кімнат
def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, template_name="bookingapp/room_list.html", context=context)


# функція представення бронювання конкретної кімнати
def book_room(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    room_id = request.GET.get('room_id')

    room = get_object_or_404(Room, id=room_id)

    context = {
        'room': room,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, template_name="bookingapp/booking.html", context=context)


# функція представення сторінки "Про нас"
def about_view(request):
    return render(request, 'bookingapp/about.html')
