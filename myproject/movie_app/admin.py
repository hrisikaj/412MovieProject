from django.contrib import admin
from .models import Actor, Director, CastCrew, Movie, User, WatchHistory, WrappedSummary

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('actor_id', 'name', 'birthyear')
    search_fields = ('name',)
    list_filter = ('birthyear',)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('director_id', 'name', 'birthyear')
    search_fields = ('name',)
    list_filter = ('birthyear',)

@admin.register(CastCrew)
class CastCrewAdmin(admin.ModelAdmin):
    list_display = ('movie_cast_id', 'movie_id', 'actor_id', 'director_id')
    search_fields = ('movie_id', 'actor_id', 'director_id')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'title', 'release_year', 'genre', 'rating')
    search_fields = ('title', 'genre')
    list_filter = ('release_year', 'genre')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'birthyear', 'profile_picture')
    search_fields = ('name', 'user_id')
    list_filter = ('birthyear',)


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('watched_id', 'user_id', 'movie_id', 'watch_date', 'rating')
    search_fields = ('user_id', 'movie_id')
    list_filter = ('watch_date',)

@admin.register(WrappedSummary)
class WrappedSummaryAdmin(admin.ModelAdmin):
    list_display = ('summary_id', 'user_id', 'top_genre', 'top_actor', 'most_watched_movie', 'total_movies_watched')
    search_fields = ('user_id', 'top_genre', 'top_actor')
    list_filter = ('top_genre',)