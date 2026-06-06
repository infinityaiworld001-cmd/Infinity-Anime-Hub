from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "infinity_anime_hub_secret"

BASE_URL = "https://api.jikan.moe/v4"
DB_NAME = "animehub.db"


def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    try:
        response = requests.get(f"{BASE_URL}/top/anime", timeout=10)
        top_anime = response.json().get("data", [])[:12]
    except Exception:
        top_anime = []

    return render_template("index.html", top_anime=top_anime)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    anime_list = []

    if query:
        try:
            response = requests.get(
                f"{BASE_URL}/anime",
                params={"q": query, "limit": 16},
                timeout=10
            )
            anime_list = response.json().get("data", [])
        except Exception:
            anime_list = []

    return render_template("search.html", anime_list=anime_list, query=query)


@app.route("/anime/<int:anime_id>")
def details(anime_id):
    try:
        response = requests.get(f"{BASE_URL}/anime/{anime_id}/full", timeout=10)
        anime = response.json().get("data", {})
    except Exception:
        anime = {}

    return render_template("details.html", anime=anime)


@app.route("/trending")
def trending():
    try:
        response = requests.get(f"{BASE_URL}/seasons/now", timeout=10)
        trending_anime = response.json().get("data", [])[:20]
    except Exception:
        trending_anime = []

    return render_template("trending.html", trending_anime=trending_anime)


@app.route("/genres")
def genres():
    genre_id = request.args.get("genre", "")
    anime_list = []

    genres_list = [
        {"id": 1, "name": "Action"},
        {"id": 2, "name": "Adventure"},
        {"id": 4, "name": "Comedy"},
        {"id": 8, "name": "Drama"},
        {"id": 10, "name": "Fantasy"},
        {"id": 14, "name": "Horror"},
        {"id": 22, "name": "Romance"},
        {"id": 24, "name": "Sci-Fi"},
        {"id": 36, "name": "Slice of Life"},
        {"id": 37, "name": "Supernatural"}
    ]

    if genre_id:
        try:
            response = requests.get(
                f"{BASE_URL}/anime",
                params={"genres": genre_id, "limit": 20},
                timeout=10
            )
            anime_list = response.json().get("data", [])
        except Exception:
            anime_list = []

    return render_template(
        "genres.html",
        genres_list=genres_list,
        anime_list=anime_list,
        genre_id=genre_id
    )


@app.route("/news")
def news():
    posts = [
        {
            "title": "One Piece Anime Seasonal Format Explained",
            "category": "Anime Updates",
            "content": "One Piece is moving toward a seasonal format with better animation quality and improved pacing."
        },
        {
            "title": "Best Anime to Watch in 2026",
            "category": "Anime Recommendations",
            "content": "Here are some popular anime series fans can watch in 2026, including action, fantasy, and adventure titles."
        },
        {
            "title": "Why Anime Fans Love Long-Running Series",
            "category": "Anime Discussion",
            "content": "Anime like One Piece, Naruto, and Bleach remain popular because of emotional characters and deep worldbuilding."
        }
    ]

    return render_template("news.html", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            flash("Account created successfully. Please login.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already exists.")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful.")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("home"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    conn = get_db()
    total_watchlist = conn.execute(
        "SELECT COUNT(*) FROM watchlist WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]
    conn.close()

    return render_template("profile.html", total_watchlist=total_watchlist)


@app.route("/add_watchlist", methods=["POST"])
def add_watchlist():
    if "user_id" not in session:
        flash("Please login to add anime to watchlist.")
        return redirect(url_for("login"))

    anime_id = request.form["anime_id"]
    title = request.form["title"]
    image_url = request.form["image_url"]
    score = request.form["score"]

    conn = get_db()

    exists = conn.execute(
        "SELECT * FROM watchlist WHERE user_id = ? AND anime_id = ?",
        (session["user_id"], anime_id)
    ).fetchone()

    if not exists:
        conn.execute(
            "INSERT INTO watchlist (user_id, anime_id, title, image_url, score) VALUES (?, ?, ?, ?, ?)",
            (session["user_id"], anime_id, title, image_url, score)
        )
        conn.commit()
        flash("Anime added to watchlist.")
    else:
        flash("Anime already in watchlist.")

    conn.close()
    return redirect(url_for("watchlist"))


@app.route("/watchlist")
def watchlist():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    conn = get_db()
    items = conn.execute(
        "SELECT * FROM watchlist WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("watchlist.html", items=items)


@app.route("/remove_watchlist/<int:item_id>")
def remove_watchlist(item_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute(
        "DELETE FROM watchlist WHERE id = ? AND user_id = ?",
        (item_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    flash("Removed from watchlist.")
    return redirect(url_for("watchlist"))


if __name__ == "__main__":
    app.run(debug=True)