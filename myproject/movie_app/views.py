from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import HttpResponse
from datetime import date
from .models import WatchHistory, Movie, WrappedSummary, User as CustomUser
from .forms import UserRegistrationForm, UserLoginForm, AddMovieForm


def index(request):
    """Home page - redirect to dashboard or login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    """User login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


def register_view(request):
    """User registration page"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create corresponding CustomUser entry
            CustomUser.objects.create(
                user_id=user.username,
                name=user.first_name or user.username,
                birthday=form.cleaned_data['birthday'],
                password=form.cleaned_data['password'],
                profile_picture=''
            )
            
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """User dashboard"""
    try:
        custom_user = CustomUser.objects.get(user_id=request.user.username)
    except CustomUser.DoesNotExist:
        custom_user = None
    
    watch_history = WatchHistory.objects.filter(
        user__user_id=request.user.username
    ).order_by('-watch_date')[:5]  # Latest 5
    
    watch_count = WatchHistory.objects.filter(
        user__user_id=request.user.username
    ).count()
    
    avg_rating = WatchHistory.objects.filter(
        user__user_id=request.user.username
    ).aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'custom_user': custom_user,
        'watch_history': watch_history,
        'watch_count': watch_count or 0,
        'avg_rating': round(avg_rating, 2) if avg_rating else 0,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def watch_history(request):
    """View full watch history"""
    watch_history = WatchHistory.objects.filter(
        user__user_id=request.user.username
    ).order_by('-watch_date')
    
    context = {
        'watch_history': watch_history,
        'total_watched': watch_history.count(),
    }
    return render(request, 'watch_history.html', context)


@login_required(login_url='login')
def add_movie(request):
    """Add a movie to watch history"""
    if request.method == 'POST':
        form = AddMovieForm(request.POST)
        if form.is_valid():
            movie = form.cleaned_data['movie']
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            watch_date = form.cleaned_data['watch_date']

            # Get or create the custom user
            custom_user, created = CustomUser.objects.get_or_create(
                user_id=request.user.username,
                defaults={
                    'name': request.user.first_name or request.user.username,
                    'birthday': date(2000, 1, 1),
                    'password': 'temp',
                    'profile_picture': ''
                }
            )

            WatchHistory.objects.create(
                user=custom_user,
                movie=movie,
                watch_date=watch_date,
                rating=rating,
                review=review
            )

            messages.success(request, f"Added '{movie.title}' to your watch history!")
            return redirect('watch_history')
    else:
        form = AddMovieForm()

    context = {'form': form}
    return render(request, 'add_movie.html', context)

@login_required(login_url='login')
def edit_watch_entry(request, entry_id):
    """Edit a watch history entry"""
    watch_entry = get_object_or_404(WatchHistory, watched_id=entry_id, user__user_id=request.user.username)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            movie_title = watch_entry.movie.title
            watch_entry.delete()
            messages.success(request, f"Deleted '{movie_title}' from your watch history!")
            return redirect('watch_history')
        else:
            form = AddMovieForm(request.POST, instance=watch_entry)
            if form.is_valid():
                form.save()
                messages.success(request, f"Updated watch history entry!")
                return redirect('watch_history')
    else:
        form = AddMovieForm(instance=watch_entry)
    
    context = {'form': form, 'entry_id': entry_id, 'watch_entry': watch_entry}
    return render(request, 'edit_watch_entry.html', context)


@login_required(login_url='login')
def wrapped_summary(request):
    """Display user's movie wrapped summary"""
    try:
        custom_user = CustomUser.objects.get(user_id=request.user.username)
        wrapped = WrappedSummary.objects.get(user=custom_user)
    except (CustomUser.DoesNotExist, WrappedSummary.DoesNotExist):
        wrapped = None
        custom_user = None
    
    # Calculate stats from watch history
    watch_history = WatchHistory.objects.filter(user__user_id=request.user.username)
    
    if watch_history.exists():
        total_movies = watch_history.count()
        avg_rating = watch_history.aggregate(Avg('rating'))['rating__avg']
        
        # Get top movie (highest rated)
        top_movie = watch_history.order_by('-rating').first()
        top_movie_title = top_movie.movie.title if top_movie else "N/A"
        
        # Get top actor (from most watched movie)
        top_actor = "N/A"
        if top_movie:
            cast_crew = top_movie.movie.castcrew_set.first()
            if cast_crew:
                top_actor = cast_crew.actor.name
        
        context = {
            'wrapped': wrapped,
            'total_movies': total_movies,
            'avg_rating': round(avg_rating, 2),
            'top_movie': top_movie_title,
            'top_actor': top_actor,
            'user_name': request.user.first_name or request.user.username,
        }
    else:
        context = {
            'wrapped': None,
            'total_movies': 0,
            'avg_rating': 0,
            'user_name': request.user.first_name or request.user.username,
            'no_data': True,
        }
    
    return render(request, 'wrapped_summary.html', context)
