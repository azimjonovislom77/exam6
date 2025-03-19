# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from .forms import CustomUserCreationForm
#
# User = get_user_model()
#
#
# def login_page(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
#             return redirect("myapp:index")
#         else:
#             messages.error(request, "Email yoki parol noto‘g‘ri!")
#
#     return render(request, 'users/login.html')
#
#
# def register_page(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('myapp:index')
#         else:
#             print(form.errors)
#     else:
#         form = CustomUserCreationForm()
#
#     return render(request, 'users/register.html', {'form': form})
#
#
# def logout_page(request):
#     logout(request)
#     return redirect("users:login_page")


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect, render

User = get_user_model()


class LoginPageView(FormView):
    template_name = 'users/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect("myapp:index")
        else:
            messages.error(request, "Email yoki parol noto‘g‘ri!")

        return render(request, self.template_name)


class RegisterPageView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class LogoutPageView(RedirectView):
    pattern_name = 'users:login_page'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
