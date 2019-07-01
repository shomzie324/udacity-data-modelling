# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
# due to mis matched song data and log data, songplays will have lots of nulls for songid and artistid, can't make it not null
# use timestamp for start_time here as well to allow fk constraint and more readable data
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays
(songplay_id serial PRIMARY KEY, start_time timestamp NOT NULL, user_id int NOT NULL, level varchar NOT NULL, song_id varchar, artist_id varchar, session_id int NOT NULL, location varchar, user_agent varchar,
FOREIGN KEY (start_time) REFERENCES time(start_time),
FOREIGN KEY(user_id) REFERENCES users(user_id),
FOREIGN KEY(song_id) REFERENCES songs(song_id),
FOREIGN KEY(artist_id) REFERENCES artists(artist_id));
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
(user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender char NOT NULL, level varchar NOT NULL);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs
(song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar NOT NULL, year int, duration numeric NOT NULL);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists
(artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, lattitude numeric, longitude numeric);
""")

# postgres has timestamp type
time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
(start_time timestamp PRIMARY KEY, hour int, day int, week int, month int, year int, weekday int);
""")

# INSERT RECORDS

# the pk is serial, so there would never be a conflict
songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, 
level, song_id, artist_id, session_id, location, user_agent)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s);
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
VALUES(%s,%s,%s,%s,%s)
ON CONFLICT (user_id) 
DO UPDATE
SET first_name=EXCLUDED.first_name, last_name=EXCLUDED.last_name,
gender=EXCLUDED.gender, level=EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
VALUES(%s,%s,%s,%s,%s)
ON CONFLICT (song_id) 
DO UPDATE
SET title=EXCLUDED.title, artist_id=EXCLUDED.artist_id, year=EXCLUDED.year, duration=EXCLUDED.duration;
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, lattitude, longitude)
VALUES(%s,%s,%s,%s,%s)
ON CONFLICT (artist_id) 
DO UPDATE
SET name=EXCLUDED.name, location=EXCLUDED.location, lattitude=EXCLUDED.lattitude, longitude=EXCLUDED.longitude;
""")


# no need to update anything, a given timestamp is always going to have the same information
time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
VALUES(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (start_time) 
DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, songs.artist_id 
FROM songs INNER JOIN artists ON songs.artist_id = artists.artist_id
WHERE songs.title = %s AND artists.name = %s AND songs.duration = %s;
""")

# QUERY LISTS

# due to fk constraints, child tables (the dimension tables) need to be created and deleted before songplays can reference/dereference them
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop, songplay_table_drop]