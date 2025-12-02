import psycopg2

conn = psycopg2.connect(
    dbname='DB_Final_Movie_Analysis',
    user='movie_log',
    password='simplePassword!',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Reset the sequence to the next value after max ID
cursor.execute("SELECT setval('watch_history_watched_id_seq', (SELECT MAX(watched_id) FROM watch_history) + 1)")
result = cursor.fetchone()
print(f"Sequence reset to: {result[0]}")

conn.commit()
cursor.close()
conn.close()
