from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CustomUserCreationForm
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from .models import CustomUser

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


# def register_page(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#
#             send_mail(
#                 'Successful Registration',
#                 'You have successfully registered on our website!',
#                 settings.EMAIL_HOST_USER,
#                 [user.email],
#                 fail_silently=False,
#             )
#
#             return redirect('myapp:index')
#         else:
#             print(form.errors)
#     else:
#         form = CustomUserCreationForm()
#
#     return render(request, 'users/register.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect("users:login_page")


class RegisterView(CreateView):
    model = User  # Agar Custom User bo'lsa, o'z modelingizni qo'ying
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'  # Ro‘yxatdan o‘tish sahifasi
    success_url = reverse_lazy('users:email_page')  # Foydalanuvchi qaysi sahifaga o'tishini belgilash

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # Email jo‘natish
        mail_subject = 'Successful Registration'
        message = render_to_string('users/email_page.html', {'user': user})

        email = EmailMessage(
            mail_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.content_subtype = "html"  # HTML formatda yuborish
        email.send()

        return redirect(self.success_url)  # `email_page` ga o'tish


class EmailPageView(TemplateView):
    template_name = 'users/email_page.html'
