from django.shortcuts import render, redirect
#Django auth system:
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #flash messages

# Create your views here.

def login_user(request):
    #Check if they filled out the form or not:
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page:
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error login in, please try again"))
            return redirect('login')
 
    else:
        return render(request, 'registration/login.html', {})