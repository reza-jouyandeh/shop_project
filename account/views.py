from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    context = {"errors": []}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        context['errors'].append('ایمیل یا گذرواژه اشتباه است')
    return render(request, "account/login.html", context)




def user_register(request):
    context = {"errors": []}
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1:
            context['errors'].append('لطفاً همه فیلدهای ضروری را پر کنید')
            return render(request, "account/register.html", context)

        if password1 != password2:
            context['errors'].append('گذرواژه‌ها با هم مطابقت ندارند')
            return render(request, "account/register.html", context)

        try:
            validate_password(password1)
        except ValidationError as exc:
            context['errors'].extend(exc.messages)
            return render(request, "account/register.html", context)

        if User.objects.filter(username=username).exists():
            context['errors'].append('این ایمیل قبلاً ثبت‌نام کرده است')
            return render(request, "account/register.html", context)

        user = User.objects.create_user(
            username=username, email=username, password=password1, first_name=fullname or ""
        )
        login(request, user)
        return redirect('/')
    return render(request, "account/register.html", context)



def user_logout(request):
    logout(request)
    return redirect('/')
