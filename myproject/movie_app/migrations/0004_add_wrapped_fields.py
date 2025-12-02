from django.db import migrations, models
from django.db.models import Avg


def forwards_func(apps, schema_editor):
    WrappedSummary = apps.get_model('movie_app', 'WrappedSummary')
    WatchHistory = apps.get_model('movie_app', 'WatchHistory')
    # Movie model to access titles
    Movie = apps.get_model('movie_app', 'Movie')

    from decimal import Decimal

    for wrapped in WrappedSummary.objects.all():
        user = wrapped.user
        wh_qs = WatchHistory.objects.filter(user_id=user.user_id)
        if not wh_qs.exists():
            wrapped.avg_rating = None
            wrapped.highest_rated_movie = None
            wrapped.save()
            continue

        avg = wh_qs.aggregate(Avg('rating'))['rating__avg']
        avg_val = Decimal(round(avg, 2)) if avg is not None else None

        top = wh_qs.order_by('-rating', '-watch_date').first()
        top_title = None
        if top and hasattr(top, 'movie'):
            try:
                top_title = top.movie.title
            except Exception:
                top_title = None

        wrapped.avg_rating = avg_val
        wrapped.highest_rated_movie = top_title
        wrapped.total_movies_watched = wh_qs.count()
        wrapped.save()


def reverse_func(apps, schema_editor):
    # On reverse, just clear the new columns
    WrappedSummary = apps.get_model('movie_app', 'WrappedSummary')
    for wrapped in WrappedSummary.objects.all():
        wrapped.avg_rating = None
        wrapped.highest_rated_movie = None
        wrapped.save()


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_castcrew_movie_user_watchhistory_wrappedsummary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wrappedsummary',
            name='avg_rating',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wrappedsummary',
            name='highest_rated_movie',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
