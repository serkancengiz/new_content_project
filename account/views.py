from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user=user)
            return redirect("home")
        else:
            return render(request, "account/login.html", {"error": "username or password is incorrect."})

    return render(request, "account/login.html")


def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {"error": "this user is already taken"})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {"error": "this email is already taken"})
                else:
                    user = User.objects.create_user(username=username, email=email, first_name=firstname,
                                                    last_name=lastname, password=password)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "account/register.html", {"error": "passwords are not the same"})

    return render(request, "account/register.html")


def logout_request(request):
    logout(request)
    return redirect("home")
