from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resource, Booking


def resource_list(request):
    resources = Resource.objects.filter(is_active=True)
    return render(request, 'bookings/resource_list.html', {'resources': resources})


@login_required(login_url='login')
def book_resource(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, id=resource_id)
        booking_date = request.POST.get('booking_date')

        exists = Booking.objects.filter(resource=resource, booking_date=booking_date).exists()

        if exists:
            messages.error(request, f"Ошибка: {resource.name} уже забронирован на {booking_date}!")
        else:
            Booking.objects.create(
                user=request.user,
                resource=resource,
                booking_date=booking_date
            )
            messages.success(request, f"Успешно! {resource.name} забронирован на {booking_date}.")

    return redirect('resource_list')


@login_required(login_url='login')
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/user_bookings.html', {'bookings': bookings})


@login_required(login_url='login')
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        booking.delete()
        messages.success(request, "Бронирование успешно отменено.")
    return redirect('user_bookings')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('resource_list')

    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        p_confirm = request.POST.get('password_confirm')

        if User.objects.filter(username=u_name).exists():
            return render(request, 'bookings/register.html', {'error': 'Этот логин уже занят'})

        if p_word != p_confirm:
            return render(request, 'bookings/register.html', {'error': 'Пароли не совпадают'})

        user = User.objects.create_user(username=u_name, password=p_word)
        auth_login(request, user)  # Сразу входим в систему
        return redirect('resource_list')

    return render(request, 'bookings/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('resource_list')

    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')

        user = authenticate(request, username=u_name, password=p_word)
        if user is not None:
            auth_login(request, user)
            return redirect('resource_list')
        else:
            return render(request, 'bookings/login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'bookings/login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('resource_list')
