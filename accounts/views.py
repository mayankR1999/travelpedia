from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

# Create your views here.
def register(request):
    if request.method == "POST":

        # unpack dictionary of input
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        user_name = request.POST["user_name"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if pass1 == pass2:
            if User.object.filter(username = user_name).exist():
                pass # pass message
            elif User.object.filter(email = email).exist():
                pass # pass message
            else:
                user = User.objects.create_user(username = user_name, email = email, password = pass1
                ,first_name = first_name, last_name = last_name)
                user.save()
        else:
            pass # pass message
        return redirect('/')

    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        pass_word = request.POST['pass']

        user = auth.authenticate(username = username, password = pass_word)
        if user:
            auth.login(request, user)
            return redirect('base/')
        else:
            pass # pass message
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')