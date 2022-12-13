from django.shortcuts import redirect, render
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from .forms import RegistrationForm,AccountForm
from django.db.models import Q

# Create your views here.
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email or Password incorrect!')
            return redirect('login')
    return render(request,'accounts/login.html')

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            if password !=confirm_password:
                messages.error(request,'Password do not match')
                return redirect('register')
            else:
                username=email.split('@')[0]
                user=Account.objects.create(email=email,first_name=first_name,last_name=last_name ,username=username)
                user.set_password(password)
                user.save()
                auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
        else:
            messages.error(request,'Email already exists')
            return redirect('register')
    else:
        form =RegistrationForm()
    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)


def logout(request):
    auth.logout(request)
    return redirect('login')

def account(request):
    if request.method=='POST':
        form=AccountForm(request.POST,instance=request.user)
        if form.is_valid():
            messages.success(request,'Updated')
            form.save()
        else:
            messages.error(request,'Email or Username already exists')
            return redirect('settings')
    else:
        form=AccountForm(instance=request.user)
    context={
        'form':form,
    }
    return render(request,'accounts/account.html',context)

def password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        user=request.user
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Updated')
                return redirect('login')
            else:
                messages.error(request,'Current password incorrect!')
                return redirect('password')
        else:
            messages.error(request,'Password do not match!')
            return redirect('password')
    return render(request,'accounts/password.html')


def search(request):
    if request.method=='GET':
        keyword=request.GET['keyword']
        people=Account.objects.filter(Q(username__icontains=keyword)|Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)).exclude(email=request.user.email)
    context={
        'people':people
    }
    return render(request,'accounts/search.html',context)