#Mariana Baker, Module 6.2 Assignment, 11/21/26
#This script connects the movies database from out last assignment and creates four queries.
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load database credentials from the .env file
secrets = dotenv_values(".env")

# Database configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

db = None
cursor = None

try:
    # Connect to the movies database
    db = mysql.connector.connect(**config)

    print(
        "\nDatabase user {} connected to MySQL on host {} "
        "with database {}".format(
            config["user"],
            config["host"],
            config["database"]
        )
    )

    cursor = db.cursor()

    # ---------------------------------------------------------
    # QUERY 1: Select all fields from the studio table
    # ---------------------------------------------------------
    print("\n\n-- DISPLAYING Studio RECORDS --")

    query1 = "SELECT * FROM studio"
    cursor.execute(query1)
    studio_records = cursor.fetchall()

    for record in studio_records:
        print("Studio ID: {}".format(record[0]))
        print("Studio Name: {}\n".format(record[1]))

    # ---------------------------------------------------------
    # QUERY 2: Select all fields from the genre table
    # ---------------------------------------------------------
    print("\n-- DISPLAYING Genre RECORDS --")

    query2 = "SELECT * FROM genre"
    cursor.execute(query2)
    genre_records = cursor.fetchall()

    for record in genre_records:
        print("Genre ID: {}".format(record[0]))
        print("Genre Name: {}\n".format(record[1]))

    # ---------------------------------------------------------
    # QUERY 3: Select movies with a runtime under two hours
    # Runtime is stored in minutes, so two hours equals 120.
    # ---------------------------------------------------------
    print("\n-- DISPLAYING Short Film RECORDS --")

    query3 = """
        SELECT film_name, film_runtime
        FROM film
        WHERE film_runtime < 120
        ORDER BY film_runtime
    """
    cursor.execute(query3)
    short_films = cursor.fetchall()

    for film in short_films:
        print("Film Name: {}".format(film[0]))
        print("Runtime: {}\n".format(film[1]))

    # ---------------------------------------------------------
    # QUERY 4: Display film names grouped by director
    # ORDER BY director places each director's films together.
    # ---------------------------------------------------------
    print("\n-- DISPLAYING Director RECORDS in Order --")

    query4 = """
        SELECT film_name, film_director
        FROM film
        ORDER BY film_director
    """
    cursor.execute(query4)
    director_records = cursor.fetchall()

    for record in director_records:
        print("Film Name: {}".format(record[0]))
        print("Director: {}\n".format(record[1]))

    input("\n\nPress any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")

    elif err.errno == errorcode.ER_NO_SUCH_TABLE:
        print("A required table does not exist. Check studio, genre, and film.")

    elif err.errno == errorcode.ER_BAD_FIELD_ERROR:
        print(
            "A column name does not match your database. Check that the "
            "film table contains film_name, film_runtime, and film_director."
        )

    else:
        print(err)

except KeyError as err:
    print(
        "A required setting is missing from your .env file: {}".format(err)
    )

finally:
    if cursor is not None:
        cursor.close()

    if db is not None and db.is_connected():
        db.close()
