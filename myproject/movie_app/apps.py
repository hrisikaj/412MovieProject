from django.apps import AppConfig


class MovieAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_app'

    def ready(self):
        """Reset PostgreSQL sequences on app startup to prevent duplicate key errors"""
        from django.db import connection

        try:
            cursor = connection.cursor()

# Reset watch_history sequence
            cursor.execute(
                "SELECT setval('watch_history_watched_id_seq', "
                "(SELECT MAX(watched_id) FROM watch_history) + 1)"
            )

            cursor.close()
        except Exception as e:
            # Silently fail if sequences don't exist yet (fresh database)
            pass