from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm

User = get_user_model()


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect("myapp:index")
        else:
            messages.error(request, "Email yoki parol noto‘g‘ri!")

    return render(request, 'users/login.html')


def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myapp:index')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect("users:login_page")
