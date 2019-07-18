from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    return render(request,'login/index.html')

def register(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        Users.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'], email=request.POST['email'],pw_hash=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()))
        messages.success(request,"Registration Complete")
        request.session['email'] = request.POST['email']
        return redirect('/success')



def login(request):
    try:
        user=Users.objects.get(email=request.POST['email'])
    except:
        messages.error(request,"User does not exist")
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
        print("password match")
        request.session['email'] = request.POST['email']
        return redirect('/success')
    else:
        print("failed password")
        return redirect('/')

def success(request):
    while 'email' in request.session:
        user=Users.objects.get(email=f"{request.session['email']}")
        context ={
        'user':user.first_name
        }
        return render(request,'login/success.html', context)
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')