from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from main.models import UserDetails
import re, random

# Create your views here.

def home(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":

        # unpack dictionary of input
        first_name, last_name = request.POST["first_name"], request.POST["last_name"]
        first_name = first_name[0].upper() + first_name[1:]
        last_name = last_name[0].upper() + last_name[1:]
        user_name = request.POST["user_name"]
        email = request.POST["email"]
        pass1, pass2 = request.POST["pass1"], request.POST["pass2"]
        
        match_special_char = re.search(r"[^A-Za-z0-9]", pass1)
        match_number = re.search(r"[0-9]", pass1)
        match_uppercase = re.search(r"[A-Z]", pass1)
        match_lowercase = re.search(r"[a-z]", pass1)
        pass_length = True if len(pass1) >= 8 else False
        
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
            
            user_details = UserDetails(user = user, username = user_name, first_name = first_name,
            last_name = last_name, full_name = first_name+ ' ' +last_name)
            user_details.save()

            return redirect('/')
        else:
            return HttpResponseRedirect(reverse('register'))

    else:
        is_guest = False
        try:
            is_guest = request.GET['is_guest']
        except Exception:
            pass

        if is_guest:
            random_number = random.randint(100000, 999999)
            username, password = 'guest'+str(random_number), "Random12#"
            first_name, last_name = 'Guest', str(random_number)
            
            new_user = User(username = username, first_name = first_name, email = str(random_number) + '@random.com',
                        last_name = last_name, password = password)
            new_user.save()

            new_user_details = UserDetails(user = new_user, username = username, first_name = first_name,
                        last_name = last_name, full_name = first_name + ' ' + last_name, is_guest = True)
            new_user_details.save()

            auth.login(request, new_user)
            return HttpResponse('')

        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        pass_word = request.POST['pass']
        user = auth.authenticate(username = username, password = pass_word)
        if user:
            auth.login(request, user)
            return redirect('../user')
        else:
            messages.info(request, "Username or password didn't match") # pass message
            return HttpResponseRedirect(reverse(login))
    else:
        return render(request, 'login.html')


def logout(request):
    concerned_username = request.user.username
    auth.logout(request)
    if UserDetails.objects.get(username = concerned_username).is_guest:
        User.objects.get(username = concerned_username).delete()
    
    return redirect('/')