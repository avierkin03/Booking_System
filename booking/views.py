from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from booking.models import Room, Booking
from datetime import datetime


# Функція для перевірки коректності дат
def check_date(start_date, end_date, room_id, request):
    if not start_date or not end_date:
        messages.error(request, "Дати заїзду та виїзду обов'язкові")
        return False
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        today = datetime.now().date()

        if start_date < today:
            messages.error(request, "Дата заїзду не може бути в минулому")
            return False
        if end_date <= start_date:
            messages.error(request, "Дата виїзду повинна бути пізніше дати заїзду")
            return False
        return True
    except ValueError:
        messages.error(request, "Некоректний формат дати")
        return False


# Функція представлення головної сторінки та пошуку кімнат
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

        # Перевіряємо коректність дат
        if start_date and end_date:
            if not check_date(start_date, end_date, None, request):
                return render(request, template_name="bookingapp/index.html", context=context)

            try:
                # Фільтруємо вільні номери
                rooms = Room.objects.exclude(bookings__start_time__lt=end_date, bookings__end_time__gt=start_date)
                # Додаємо додаткові фільтри, якщо вони вказані
                if quantity:
                    rooms = rooms.filter(capacity__gte=int(quantity))
                if price_from:
                    rooms = rooms.filter(price__gte=float(price_from))
                if price_to:
                    rooms = rooms.filter(price__lte=float(price_to))
            except ValueError:
                rooms = Room.objects.all()  # Повертаємо всі номери при помилці

        # Оновлюємо контекст із введеними даними
        context.update({
            'rooms': rooms,
            'start_date': start_date,
            'end_date': end_date,
            'quantity': quantity,
            'price_from': price_from,
            'price_to': price_to,
            'filtered': bool(start_date and end_date)
        })

    return render(request, template_name="bookingapp/index.html", context=context)


# Функція представлення списку всіх кімнат
def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, template_name="bookingapp/room_list.html", context=context)


# Функція представлення бронювання конкретної кімнати
@login_required(login_url="/login/")
def book_room(request):
    if request.method == "GET":
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        room_id = request.GET.get('room_id')

        if not room_id:
            messages.error(request, "ID кімнати не вказано")
            return redirect("index")

        room = get_object_or_404(Room, id=room_id)
        context = {
            'room': room,
            'room_id': room_id,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Перевіряємо коректність дат
        if not start_date or not end_date:
            messages.error(request, "Дата початку та кінця бронювання обов'язкові")
            return render(request, template_name="bookingapp/booking.html", context=context)

        if not check_date(start_date, end_date, room_id, request):
            return redirect("index")  # Перенаправлення на головну сторінку при некоректних датах

        return render(request, template_name="bookingapp/booking.html", context=context)
    
    elif request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        room_id = request.POST.get('room_id')

        if not room_id:
            messages.error(request, "ID кімнати не вказано")
            return redirect("index")

        room = get_object_or_404(Room, id=room_id)
        context = {
            'room': room,
            'start_date': start_date,
            'end_date': end_date,
            'room_id': room_id,
        }

        # Перевірка, чи заповнені поля
        if not start_date or not end_date:
            messages.error(request, "Дата початку та кінця бронювання обов'язкові")
            return render(request, template_name="bookingapp/booking.html", context=context)
        
        # Перевірка коректності дат
        if not check_date(start_date, end_date, room_id, request):
            return render(request, template_name="bookingapp/booking.html", context=context)

        # Перевірка, чи номер зайнятий
        if Booking.objects.filter(room=room, start_time__lt=end_date, end_time__gt=start_date).exists():
            messages.error(request, "Номер зайнятий на вибрані дати")
            return render(request, template_name="bookingapp/booking.html", context=context)
            
        # Створюємо нове бронювання
        try:
            booking = Booking.objects.create(
                user=request.user,
                room=room,
                start_time=start_date,
                end_time=end_date,
            )
            messages.success(request, "Бронювання успішно створено!")
            context = {'room': room, 'booking': booking}
            return render(request, "bookingapp/booking_success.html", context)
        except ValueError as e:
            messages.error(request, f"Помилка при створенні бронювання: {str(e)}")
            return render(request, template_name="bookingapp/booking.html", context=context)


# Функція представлення сторінки "Історія бронювань"
@login_required(login_url="/login/")
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'bookingapp/booking_history.html', {'bookings': bookings})


# Функція представлення сторінки "Про нас"
def about_view(request):
    return render(request, 'bookingapp/about.html')