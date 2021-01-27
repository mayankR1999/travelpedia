from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
import re

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
        
        match_special_char = re.search(r"[^A-Za-z0-9]", pass1)
        match_number = re.search(r"[0-9]", pass1)
        match_uppercase = re.search(r"[A-Z]", pass1)
        match_lowercase = re.search(r"[a-z]", pass1)
        pass_length = True if len(pass1 >= 8) else False
        
        valid = True

        if len(user_name) < 4:
            valid = False
            messages.info(request, 'invalid username, must contain atleast 4 letters.')
        if User.objects.filter(username = user_name).exists():
            valid = False
            messages.info(request, 'username already exists.')
        if User.objects.filter(email = email).exists():
            valid = False
            messages.info(request, 'email already associated with an account.')
        if pass1 != pass2:
            valid = False
            messages.info(request, 'passwords do not match.')
        if not match_lowercase or not match_number or not match_special_char or not match_uppercase or not pass_length:
            valid = False
            messages.info(request, 'password should contain atleast a number, must contain atleast 8 characters,'
                                    + ' an special character, a lowercase and an uppercase letter.')
        if valid is True:
            user = User.objects.create_user(username = user_name, email = email, password = pass1
            ,first_name = first_name, last_name = last_name)
            user.save()
            return redirect('/')
        else:
            return HttpResponseRedirect(reverse('register'))

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
            messages.info(request, "Username or password didn't match") # pass message
            return HttpResponseRedirect(reverse(login))
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')