from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField()

    def __str__(self):
        return self.title
    
class actors(models.Model):
    actor_id = models.IntegerField(primary_key=True)   # existing PK
    name = models.CharField(max_length=100)
    birthyear = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.birthyear})"
    
class directors(models.Model):
    director_id = models.IntegerField(primary_key=True)  # existing PK
    name = models.CharField(max_length=100)
    birthyear = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.birthyear})"

class movies(models.Model):
    movie_id = models.AutoField(primary_key=True)  # existing PK
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    plot = models.TextField()
    runtime = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class cast_crew(models.Model):
    movie_cast_id = models.AutoField(primary_key=True)  # existing PK
    movie_id = models.IntegerField()
    actor_id = models.IntegerField()
    director_id = models.IntegerField()

    def __str__(self):
        return f"Movie ID: {self.movie_id}, Actor ID: {self.actor_id}, Director ID: {self.director_id}"

class users(models.Model):
    user_id = models.CharField(max_length=100) # existing PK
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    birthday = models.IntegerField()
    profile_picture = models.CharField(max_length=200)

    def __str__(self):
        return self.username
    
class watch_history(models.Model):
    watched_id = models.AutoField(primary_key=True)  # existing PK
    user_id = models.CharField(max_length=100)
    movie_id = models.IntegerField()
    watch_date = models.DateField()
    rating = models.FloatField()
    review = models.TextField()

    def __str__(self):
        return f"User ID: {self.user_id}, Movie ID: {self.movie_id}, Watch Date: {self.watch_date}"

class wrapped_summary(models.Model):
    summary_id = models.AutoField(primary_key=True)  # existing PK
    user_id = models.CharField(max_length=100)
    top_genre = models.CharField(max_length=100)
    top_actor = models.CharField(max_length=100)
    most_watched_movie = models.CharField(max_length=200)
    total_movies_watched = models.IntegerField()

    def __str__(self):
        return f"User ID: {self.user_id}, Top Genre: {self.top_genre}, Top Actor: {self.top_actor}, Most Watched Movie: {self.most_watched_movie}"