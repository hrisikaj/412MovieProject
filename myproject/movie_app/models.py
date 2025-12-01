from django.db import models

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    plot = models.TextField()
    runtime = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    class Meta:
        db_table = 'movies'  # Point to existing 'movies' table
    

class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True, db_column='birth_year')

    def __str__(self):
        return f"{self.name} ({self.birth_year})"
    
    class Meta:
        db_table = 'actors'  # Point to existing 'actors' table

class Director(models.Model):
    director_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True, db_column='birth_year')

    def __str__(self):
        return f"{self.name} ({self.birth_year})"
    
    class Meta:
        db_table = 'directors'  # Point to existing 'directors' table

class CastCrew(models.Model):
    movie_cast_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} - {self.actor.name} - {self.director.name}"
    
    class Meta:
        db_table = 'cast_crew'  # Point to existing 'cast_crew' table

class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    birthday = models.DateField(db_column='birthday')
    profile_picture = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'users'  # Point to existing 'users' table

class WatchHistory(models.Model):
    watched_id = models.AutoField(primary_key=True, db_column='watched_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_date = models.DateField()
    rating = models.FloatField()
    review = models.TextField()

    def __str__(self):
        return f"{self.user.name} watched {self.movie.title} on {self.watch_date}"
    
    class Meta:
        db_table = 'watch_history'  # Point to existing 'watch_history' table

class WrappedSummary(models.Model):
    summary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top_genre = models.CharField(max_length=100)
    top_actor = models.CharField(max_length=100)
    most_watched_movie = models.CharField(max_length=200)
    total_movies_watched = models.IntegerField()

    def __str__(self):
        return f"{self.user.name}'s summary"
    
    class Meta:
        db_table = 'wrapped_summary'  # Point to existing 'wrapped_summary' table