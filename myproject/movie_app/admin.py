from django.contrib import admin
from .models import Actor, Director, CastCrew, Movie, User, WatchHistory, WrappedSummary

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('actor_id', 'name', 'birth_year')
    search_fields = ('name',)
    list_filter = ('birth_year',)

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('director_id', 'name', 'birth_year')
    search_fields = ('name',)
    list_filter = ('birth_year',)

@admin.register(CastCrew)
class CastCrewAdmin(admin.ModelAdmin):
    list_display = ('movie_cast_id', 'movie_id', 'actor_id', 'director_id')
    search_fields = ('movie_id', 'actor_id', 'director_id')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'title', 'release_year', 'runtime')
    search_fields = ('title',)
    list_filter = ('release_year',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'birthday', 'profile_picture')
    search_fields = ('name', 'user_id')
    list_filter = ('birthday',)


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