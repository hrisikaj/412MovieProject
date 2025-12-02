from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0004_add_wrapped_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wrappedsummary',
            name='top_genre',
        ),
        migrations.RemoveField(
            model_name='wrappedsummary',
            name='most_watched_movie',
        ),
    ]
