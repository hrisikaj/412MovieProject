Setting up the database
First: Right Click Databases > Create > Database
	Name: DB_Final_Movie_Analysis
Author: your auth name
Then, on the URL bar above the folder and save buttons, 

Go ahead and click new connection
Make sure that database says DB_Final_Movie_Analysis, then hit Save. This should open an SQL page for you to paste and run sql codes. (You can also right click the database and open query tool to do this).
Paste and run the below:
-- USERS Table
CREATE TABLE users (
    user_id VARCHAR (16) PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    profile_picture TEXT
);
-- ACTOR Table: List of unique actors in all of the movies
CREATE TABLE actors (
    actor_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_year INT CHECK (birth_year > 1900)
);
-- DIRECTOR Table: List of unique directors in all movies
CREATE TABLE directors (
    director_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_year INT CHECK (birth_year > 1900)
);
-- MOVIE Table: List of unique movies
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INT CHECK (release_year > 1900),
    plot TEXT,
    runtime INT CHECK (runtime > 0)
);
-- CAST_CREW Table: This table is a list of cast and directors with respect to a movie
CREATE TABLE cast_crew (
    movie_cast_id SERIAL PRIMARY KEY,
    movie_id INT,
    actor_id INT,
    director_id INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id) ON DELETE CASCADE,
    FOREIGN KEY (director_id) REFERENCES directors(director_id) ON DELETE CASCADE
);
-- WATCH_HISTORY Table: This table is a list of movies linked to the user that watched them
CREATE TABLE watch_history (
    watched_id SERIAL PRIMARY KEY,
    user_id VARCHAR(16),
    movie_id INT,
    watch_date DATE NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 10),
    review TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
);
-- WRAPPED_SUMMARY Table: This table is a list of summaries of analytics per user
CREATE TABLE wrapped_summary (
    summary_id SERIAL PRIMARY KEY,
    user_id VARCHAR(16),
    top_actor TEXT,
    total_movies_watched INT,
    avg_rating NUMERIC(4,2),
    highest_rated_movie VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

Next, download the csv files: (https://drive.google.com/drive/folders/1-P0WzzvtsKSSYY2oq_9Q8FShtWSUU1dQ?usp=drive_link).
Right click each table, hit import data, select the respective csv files from your file explorer. Make sure the delimiter is set to comma and header is checked. 

Upload cast_crew, watch_history, and wrapped_summary last. 

You also want to create a user for this application; in this case, that is movie_log.
To do this in pgAdmin, scroll to the bottom of your Object Explorer, to  Login/Group Roles. Right click and create. 

Here, you can name the user movie_log, then set the password to simplePassword! under the Definition tab. After this, you set the privileges to superuser and can login, then hit ‘Save’. This should sum up any set up in pgAdmin. 

Setting up the application
	Download the files as zip, extract, and open folder in IDE. 
Make sure to download the .env file (not in the github repo) (https://drive.google.com/file/d/1RpwBH6ZL9yFrVnLDI0BHpFK7i95GaOnK/view?usp=drive_link), and place this in the same directory as manage.py. 
After downloading the .env file, it may be renamed to “env”. It is important that the file has the “.” , so after placing in same directory as manage.py, rename it to 
“.env”
Make sure your database name, user and password in the .env file match the ones you created in pgAdmin. 
Then initialize the virtual environment (follow respective instructions for Windows or Mac).
After initializing the virtual environment, install the requirements using:
“pip install -r requirements.txt” 
Next, you want to change directories into the myproject folder:
cd .\myproject\
Make sure to do python manage.py migrate to make sure that your database information is correctly imported into your compiler.
Create a superuser by putting python manage.py createsuperuser in the terminal, and creating a user to access the admin panel with. This can be whatever username and password you’d like. This superuser will have access to the front end app as well. 
Any non-admin accounts can be created using the “Register” button in the website’s dashboard. 
Running the application
In the terminal, use python manage.py runserver to run the application. 
In order to view the admin panel AND the dashboard, use the login from the superuser you created in the previous step. 
To access the admin panel, go to /admin. / should reroute to login or dashboard if admin is already logged into. 
