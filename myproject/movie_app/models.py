from django.db import models

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    plot = models.TextField()
    runtime = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.release_year})"

class Actor(models.Model):
    actor_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    birthyear = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.birthyear})"

class Director(models.Model):
    director_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    birthyear = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.birthyear})"

class CastCrew(models.Model):
    movie_cast_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} - {self.actor.name} - {self.director.name}"

class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    birthyear = models.IntegerField()
    profile_picture = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class WatchHistory(models.Model):
    watched_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_date = models.DateField()
    rating = models.FloatField()
    review = models.TextField()

    def __str__(self):
        return f"{self.user.name} watched {self.movie.title} on {self.watch_date}"

class WrappedSummary(models.Model):
    summary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    top_genre = models.CharField(max_length=100)
    top_actor = models.CharField(max_length=100)
    most_watched_movie = models.CharField(max_length=200)
    total_movies_watched = models.IntegerField()

    def __str__(self):
        return f"{self.user.name}'s summary"