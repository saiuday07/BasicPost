from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, PostForm
from django.contrib.auth import authenticate, login, logout
from .models import post
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
    name = 'SaiUday'
    nums = [1, 3, 5, 8, 13, 19]
    context = {'name': name, 'nums': nums}
    return render(request, 'home.html', context)

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        #request.POST is a dictionary containing the form data submitted by the user.
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

def register(request):

    if request.method == 'GET':
        form = UserRegistrationForm() #empty registration form
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        #request.POST is a dictionary containing the form data submitted by the user. 
        # It includes the values of the form fields, such as username, email, password1, and password2.
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save() #create user in the database
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
        
def user_logout(request):
    logout(request)
    return redirect('home')

def posts(request):
    post_list=post.objects.all().order_by('-updated_at')  #select * from posts.
    return render(request,'posts.html',{'post_list':post_list})

def read_post(request,id):
    Post=post.objects.get(pk=id)                               #pk=primary key
    return render(request,'read-post.html',{'post':Post})

@login_required(login_url='login')
def create_post(request):
    form=PostForm()    #emptyform
    if request.method=='GET':
        return render(request,'create-post.html',{'form':form})
    
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            Post=form.save(commit=False) 
            Post.author= request.user   #assaign user as author 
            Post.save()     # Create post
            return redirect('posts')
        else:
            return render(request, 'create-post.html', {'form': form})
        
def update_post(request,id):
    try:
        Post=post.objects.get(pk=id)
    except post.DoesNotExist:
        return redirect('posts')

    
    if request.user !=post.author:
        return redirect('posts')
    
    form=PostForm(instance=Post)

    if request.method=='GET':
        return render(request,'update-post.html',{'form':form})
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            Post=form.save(commit=False) 
            Post.author= request.user   #assaign user as author 
            Post.save()     # Create post
            return redirect('posts')
        else:
            return render(request, 'update-post.html', {'form': form})

def delete_post(request,id):
    try:
        Post=post.objects.get(pk=id)
    except post.DoesNotExist:
        return redirect('posts')

    if request.user!=post.author:
        return redirect('posts')
    
    Post.delete()
    return redirect('posts')