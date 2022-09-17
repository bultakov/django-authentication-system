from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView


class LogIn(LoginView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request=request, message="Foydalanuvchi topilmadi!!!")
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request=request, message="Noto'g'ri parol kiritilgan")
            return redirect('login')
        login(request=request, user=user)
        if not rememberme:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        messages.success(request=request, message="Success")
        return redirect('success')


class SignUp(CreateView):
    model = User
    fields = "__all__"
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        try:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')

            if password1 != password2:
                messages.success(request, 'Ikkala parol maydonidagi parollar bir xil emas!!!')
                return redirect('signup')

            if User.objects.filter(username=username).first():
                messages.success(request, "Bunday foydalanuvchi avvalroq ro'yxatdan o'tgan!!!")
                return redirect('signup')

            if User.objects.filter(email=email).first():
                messages.success(request, "Bu email avvalroq ro'yxatdan o'tgan!!!")
                return redirect('signup')

            user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user_obj.set_password(raw_password=password1)
            user_obj.save()
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Xatolik {e}")
            return redirect('signup')


def success(request):
    return render(request=request, template_name='success.html', context={})


def user_logout(request):
    logout(request)
    return redirect(to='login')
