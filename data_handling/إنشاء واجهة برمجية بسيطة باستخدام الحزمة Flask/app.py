from flask import Flask, request, abort
import mysql.connector


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="0000",
    database="sakila",
    port="3306",
)

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>hello world</h1>"


# ===========================================================
def get_results(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, *args)
    result = cursor.fetchall()
    cursor.close()
    return result if result else abort(404)


def get_one_result(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, *args)
    result = cursor.fetchone()
    cursor.close()
    return result if result else abort(404)


# ===========================================================


@app.get("/actors")
def get_all_actors():
    query = "SELECT actor_id, first_name, last_name FROM actor"
    rssult = get_results(query=query)
    return rssult


@app.get("/actors/<int:actor_id>")
def get_one_actor(actor_id):
    query = "SELECT actor_id, first_name, last_name FROM actor WHERE actor_id = %s"
    result = get_one_result(query, (actor_id,))
    return result


# ===========================================================
@app.get("/films")
def get_film_by_rating():
    ratings = request.args["rating"].split(",")
    query_placeholder = ",".join(["%s"] * len(ratings))
    query = (
        "SELECT film_id, title, description, rental_rate, rating FROM film WHERE rating in (%s)"
        % query_placeholder
    )
    result = get_results(query, ratings)
    return result if result else {"error": "404"}


@app.get("/films/<int:film_id>")
def get_one_film(film_id):
    query = """SELECT  f.film_id, f.title, f.description, c.name, f.rental_rate FROM film as f 
join film_category as fc on f.film_id = fc.film_id
join category as c on c.category_id = fc.category_id
Having f.film_id = %s"""

    result = get_one_result(query, (film_id,))
    return result if result else abort(404)


# ===========================================================
if __name__ == "__main__":
    app.run(debug=True)
