from django.shortcuts import render, redirect
#Django auth system:
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #flash messages
#Registration form (included in django)
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.views import generic
from django.urls import reverse_lazy


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
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You've been successfully logged out"))
    return redirect ('home')

# def register_user(request):
#     if request.method=='POST':
#         form = UserCreationForm(request.POST) #filled out form
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request,user)
#             messages.success(request,('Registration successful'))
#             return redirect('home')
#         else:
#             form = UserCreationForm() #empty form
        
#         return render(request, 'registration/register_user.html',{'form':form,})

class UserRegisterView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('login')