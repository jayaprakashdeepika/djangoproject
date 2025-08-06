from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import RegisterForm, ProfileForm
from .models import Blog, Comment

# ✅ Home - Show all blogs to logged-in users only
@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')

    # ✅ Pagination
    paginator = Paginator(blogs, 3)  # Show 3 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj, 'query': query})

# ✅ Register
def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            #login(request, user)
            return redirect('login')
    else:
        user_form = RegisterForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'form': user_form, 'profile_form': profile_form})

# ✅ Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# ✅ Logout
def logout_user(request):
    logout(request)
    return redirect('login')

# ✅ Create Blog
@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if title and content:
            Blog.objects.create(
                title=title,
                content=content,
                image=image,
                author=request.user
            )
            return redirect('home')
    return render(request, 'create_blog.html')

# ✅ Edit Blog
@login_required
def edit_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, author=request.user)
    except Blog.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return redirect('home')

    return render(request, 'edit_blog.html', {'blog': blog})

# ✅ Delete Blog
@login_required
def delete_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, author=request.user)
        blog.delete()
    except Blog.DoesNotExist:
        pass
    return redirect('home')

# ✅ Comment on Blog
@login_required
def comment_blog(request, blog_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            try:
                blog = Blog.objects.get(id=blog_id)
                Comment.objects.create(blog=blog, author=request.user, text=text)
            except Blog.DoesNotExist:
                pass
    return redirect('home')

# ✅ Simple password reset
def simple_reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            return render(request, 'simple_reset.html', {'error': "Passwords don't match"})
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            return render(request, 'simple_reset.html', {'error': "Username not found"})
    return render(request, 'simple_reset.html')
