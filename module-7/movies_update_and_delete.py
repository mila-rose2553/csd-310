# Author: Mariana Baker
# 7.2 Assignment: Movies Update and Delete
# Purpose: Insert, update, and delete movie records in the movies database.

from pathlib import Path

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values


# Load the .env file from the same folder as this Python file.
script_folder = Path(__file__).resolve().parent
env_path = script_folder / ".env"

# Use the uploaded .env(1) filename if it has not been renamed yet.
if not env_path.exists():
    env_path = script_folder / ".env(1)"

secrets = dotenv_values(env_path)

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": str(
        secrets.get("RAISE_ON_WARNINGS", "True")
    ).lower() == "true"
}


def show_films(cursor, title):
    """Display each film in the same vertical format as the assignment example."""
    print("\n -- " + title + " --")

    query = """
        SELECT
            film.film_name,
            film.film_director,
            genre.genre_name,
            studio.studio_name
        FROM film
        INNER JOIN genre
            ON film.genre_id = genre.genre_id
        INNER JOIN studio
            ON film.studio_id = studio.studio_id
        ORDER BY film.film_name
    """

    cursor.execute(query)

    for film in cursor.fetchall():
        print("Film Name: " + str(film[0]))
        print("Director: " + str(film[1]))
        print("Genre Name: " + str(film[2]))
        print("Studio Name: " + str(film[3]))
        print()


db = None
cursor = None

try:
    # Connect to the movies database.
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # 1. Display the original films.
    show_films(cursor, "DISPLAYING FILMS")

    # 2. Insert a new film. Use an existing studio and genre.
    # Do not insert the film again if this script has already been run.
    insert_query = """
        INSERT INTO film
            (film_name, film_releaseDate, film_runtime,
             film_director, studio_id, genre_id)
        SELECT
            %s, %s, %s, %s, studio.studio_id, genre.genre_id
        FROM studio
        CROSS JOIN genre
        WHERE studio.studio_name = %s
          AND genre.genre_name = %s
          AND NOT EXISTS (
              SELECT 1
              FROM film
              WHERE film_name = %s
          )
        LIMIT 1
    """

    cursor.execute(
        insert_query,
        (
            "The Visit",
            "2015",  # Store the year only; film_releaseDate is a year-sized field
            94,
            "M. Night Shyamalan",
            "20th Century Fox",
            "Horror",
            "The Visit"
        )
    )
    db.commit()

    if cursor.rowcount == 1:
        print("\nSuccessfully inserted The Visit.")
    else:
        print("\nThe Visit already exists or the selected studio/genre was not found.")

    # 3. Display films after INSERT.
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # 4. Update Alien to the Horror genre.
    update_query = """
        UPDATE film
        SET genre_id = (
            SELECT genre_id
            FROM genre
            WHERE genre_name = %s
        )
        WHERE film_name = %s
    """

    cursor.execute(update_query, ("Horror", "Alien"))
    db.commit()

    # 5. Display films after UPDATE.
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    # 6. Delete Gladiator.
    delete_query = """
        DELETE FROM film
        WHERE film_name = %s
    """

    cursor.execute(delete_query, ("Gladiator",))
    db.commit()

    # 7. Display films after DELETE.
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid MySQL username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The movies database does not exist.")
    else:
        print("MySQL Error:", err)

except (KeyError, TypeError) as err:
    print("Configuration error. Check that the .env file contains USER, PASSWORD, HOST, and DATABASE.")
    print(err)

finally:
    if cursor is not None:
        cursor.close()

    if db is not None and db.is_connected():
        db.close()
        print("\nDatabase connection closed.")
