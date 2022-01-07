CREATE TABLE IF NOT EXISTS Songs (
    id integer PRIMARY KEY,
    title varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS Sounds_in_songs (
    song_id integer NOT NULL,
    sound_number integer NOT NULL,
    sound_name varchar NOT NULL,
    sound_length float NOT NULL,
    FOREIGN KEY(song_id) REFERENCES Songs(id)
);

-- In the case of most melodies:
-- 0.5 = eighth 
-- 1 = quarter note
-- 2 = half note
-- 3 = dotted half note
-- 4 = whole note


INSERT INTO Songs (id, title) VALUES (0, "Star Wars Theme");
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 0, "C1", 4);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 1, "G1", 4);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 2, "F1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 3, "E1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 5, "D1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 5, "C2", 4);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 6, "G1", 4);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 7, "F1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 8, "E1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 9, "D1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 10, "C2", 4);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 11, "G1", 4);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 12, "F1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 13, "E1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 14, "F1", 1);
INSERT INTO Sounds_in_songs (song_id, sound_number, sound_name, sound_length) VALUES (0, 15, "D1", 4);


