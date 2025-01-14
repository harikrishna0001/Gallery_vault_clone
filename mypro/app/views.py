from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Gallery

# Home page displaying images
@login_required
def index(request):
    feeds = Gallery.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "index.html", {"feeds": feeds})

# User login
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Both username and password are required!")
            return render(request, 'signin.html')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/index/')
            if not next_url.startswith('/'):
                next_url = '/index/'  # fallback to a safe internal URL
            return redirect(next_url)
        
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'signin.html')

# User registration (signup)
def usersignup(request):
    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        print(email,username,password,confirmpassword)
        if not all([email, username, password, confirmpassword]):
            messages.error(request, 'All fields are required.')
        elif password != confirmpassword:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully!")
            return redirect('signin')
    
    return render(request, "createuser.html")

# User logout
def logoutuser(request):
    logout(request)
    return redirect('signin')

# Add a new image post
@login_required
def addimage(request):
    if request.method == 'POST':
        feedimage = request.FILES.get('feedimage')
        if feedimage:
            Gallery.objects.create(feedimage=feedimage, user=request.user)
            messages.success(request, "Image added successfully.")
            return redirect("index")
        else:
            messages.error(request, "Please upload an image.")
    
    return render(request, "newpost.html")

# View a specific image
def view_image(request, pk):
    feed = get_object_or_404(Gallery, pk=pk)
    return render(request, "image.html", {"feed": feed})

# Delete an image
@login_required
def delete_image(request, pk):
    feed = get_object_or_404(Gallery, pk=pk)
    
    if feed.user == request.user:  # Only allow image deletion by the user who uploaded it
        feed.delete()
        messages.success(request, "Image deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this image.")
    
    return redirect('index')
