from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
from .models import WatchHistory, Movie, WrappedSummary, User as CustomUser, Actor
from .forms import UserRegistrationForm, UserLoginForm, AddMovieForm


def _recompute_wrapped_summary_for_user(custom_user):
    """Recompute and persist WrappedSummary values for a given CustomUser."""
    if not custom_user:
        return
    user_id = custom_user.user_id
    # gather watch history
    wh_qs = WatchHistory.objects.filter(user__user_id=user_id)
    
    avg = wh_qs.aggregate(Avg('rating'))['rating__avg']
    avg_val = Decimal(round(avg, 2)) if avg is not None else None

    if wh_qs.exists():
        top = wh_qs.order_by('-rating', '-watch_date').first()
        top_title = top.movie.title if top else None
        total_count = wh_qs.count()
        
        # Calculate top actor - find the actor that appears most in user's watched movies
        top_actor_obj = (
            Actor.objects
            .filter(castcrew__movie__watchhistory__user__user_id=user_id)
            .annotate(appearance_count=Count('castcrew'))
            .order_by('-appearance_count')
            .first()
        )
        top_actor = top_actor_obj.name if top_actor_obj else 'N/A'
    else:
        top_title = None
        total_count = 0
        top_actor = 'N/A'

    # Try to get existing row, if not found create
    try:
        wrapped = WrappedSummary.objects.get(user=custom_user)
        wrapped.avg_rating = avg_val
        wrapped.highest_rated_movie = top_title
        wrapped.total_movies_watched = total_count
        wrapped.top_actor = top_actor
        wrapped.save()
    except WrappedSummary.DoesNotExist:
        # Only create if doesn't exist
        WrappedSummary.objects.create(
            user=custom_user,
            top_actor=top_actor,
            total_movies_watched=total_count,
            avg_rating=avg_val,
            highest_rated_movie=top_title,
        )


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
            custom_user = CustomUser.objects.create(
                user_id=user.username,
                name=user.first_name or user.username,
                birthday=form.cleaned_data['birthday'],
                password=form.cleaned_data['password'],
                profile_picture=''
            )
            
            # Create default WrappedSummary entry with null/NA/0 values
            WrappedSummary.objects.create(
                user=custom_user,
                top_actor='N/A',
                total_movies_watched=0,
                avg_rating=None,
                highest_rated_movie=None
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
            
            # Recompute user's wrapped summary after adding an entry
            _recompute_wrapped_summary_for_user(custom_user)

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
            custom_user = watch_entry.user
            watch_entry.delete()
            # Recompute summary after deletion
            _recompute_wrapped_summary_for_user(custom_user)
            messages.success(request, f"Deleted '{movie_title}' from your watch history!")
            return redirect('watch_history')
        else:
            form = AddMovieForm(request.POST, instance=watch_entry)
            if form.is_valid():
                form.save()
                # Recompute summary after edit
                _recompute_wrapped_summary_for_user(watch_entry.user)
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
        return render(request, 'wrapped_summary.html', {'no_data': True, 'user_name': request.user.first_name or request.user.username})
    
    # Check if user has watch history
    watch_history = WatchHistory.objects.filter(user__user_id=request.user.username)
    
    if not watch_history.exists():
        context = {
            'no_data': True,
            'user_name': request.user.first_name or request.user.username,
        }
    else:
        # Use persisted values from WrappedSummary
        total_movies = wrapped.total_movies_watched or 0
        avg_rating = float(wrapped.avg_rating) if wrapped.avg_rating else 0
        top_movie_title = wrapped.highest_rated_movie or "N/A"
        top_actor = wrapped.top_actor or "N/A"
        
        context = {
            'wrapped': wrapped,
            'total_movies': total_movies,
            'avg_rating': round(avg_rating, 2) if avg_rating else 0,
            'top_movie': top_movie_title,
            'top_actor': top_actor,
            'user_name': request.user.first_name or request.user.username,
        }
    
    return render(request, 'wrapped_summary.html', context)
