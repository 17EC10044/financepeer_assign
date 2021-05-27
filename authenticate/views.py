from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import json
import os
from mysite.settings import BASE_DIR

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'templates/home.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'authenticate/home.html')

from .models import File

def validateJSON(filename):
    with open(filename) as f:
    	return json.load(f)

def home(request):
	if request.method=='POST' and request.FILES['myfile']:
		myfile=request.FILES['myfile']
		
		
		fs=FileSystemStorage()
		filename=fs.save(myfile.name,myfile)
		

		uploaded_file_url=fs.url(filename)
		f=fs.open(BASE_DIR+uploaded_file_url)
		if validateJSON(BASE_DIR+uploaded_file_url)==False:
			messages.success(request, ('Error Invalid JSON - Choose Another File...'))
			return redirect('home')

		json_data=json.load(f)
		parsed_data=File(data=json_data)
		#print(parsed_data.data)
		parsed_data.save()
		stu = {
    	"File_number": parsed_data.data
		}
		return render(request,'authenticate/data.html',stu)
		
	
	return render(request, 'authenticate/home.html', {})






def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Been Logged In!'))
			return redirect('home')

		else:
			messages.success(request, ('Error Logging In - Please Try Again...'))
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('You Have Been Logged Out...'))
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('You Have Registered...'))
			return redirect('home')
	else:
		form = SignUpForm()
	
	context = {'form': form}
	return render(request, 'authenticate/register.html', context)



def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You Have Edited Your Profile...'))
			return redirect('home')
	else:
		form = EditProfileForm(instance=request.user)
	
	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Edited Your Password...'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)
	
	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)





#from django.shortcuts import render
from .models import File
from .forms import FileForm

def showfile(request):
	if request.method=='GET':
		return render(request,'authenticate/home.html')	
	lastfile=File.objects.last()
	data=lastfile.data
	form=FileForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
	context={'data':data,'form':form}
	return render(request,'authenticate/home.html',context)

