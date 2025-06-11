from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from auth_system.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm


# функція, яка відповідає за реєстрацію нашого користувача
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()

    return render(request, template_name="auth_system/register.html", context={'form': form})


# функція, яка дозволяє працювати з логіном користувача
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Неправильний логін та пароль")
    else:
        form = AuthenticationForm()

    return render(request, template_name="auth_system/login.html", context={'form': form})


# Нова функція для виходу
def user_logout(request):
    logout(request)  # Виконує вихід користувача
    messages.success(request, "Ви успішно вийшли з системи.")
    return redirect('index')