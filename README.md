# 🎌 Infinity Anime Hub

Infinity Anime Hub is a modern anime discovery platform built using Python Flask. The website allows users to search anime, view detailed information, explore trending series, filter by genres, save favorites to a personal watchlist, and read anime news updates.

This project was created as a learning project to improve web development skills using Flask, SQLite, HTML, CSS, JavaScript, and API integration.

---

## 🚀 Features

### 🔍 Anime Search

Search anime titles instantly using the Jikan API.

### 📖 Anime Details

View:

* Anime Title
* Poster Image
* Rating Score
* Episode Count
* Anime Type
* Duration
* Genres
* Synopsis

### 🎬 Anime Trailer

Watch official anime trailers directly from the details page.

### 🔥 Trending Anime

Discover currently trending and popular anime series.

### 🎭 Genre Filter

Browse anime by genres:

* Action
* Adventure
* Comedy
* Drama
* Fantasy
* Horror
* Romance
* Sci-Fi
* Slice of Life
* Supernatural

### 👤 User Account System

* Register Account
* Login
* Logout
* Secure Password Storage

### ❤️ Anime Watchlist

Users can:

* Add Anime to Watchlist
* View Saved Anime
* Remove Anime from Watchlist

### 📰 Anime News Section

Read anime-related articles, updates, and recommendations.

### 👤 User Profile

View:

* Username
* User ID
* Total Watchlist Count

---

## 🛠 Technologies Used

### Backend

* Python
* Flask
* SQLite3
* Requests
* Werkzeug

### Frontend

* HTML5
* CSS3
* JavaScript

### API

* Jikan API

The Jikan API provides anime information from MyAnimeList.

---

## 📂 Project Structure

```text
Infinity_Anime_Hub/

│ app.py
│ animehub.db
│ README.md

├── templates/
│   ├── index.html
│   ├── search.html
│   ├── details.html
│   ├── login.html
│   ├── register.html
│   ├── watchlist.html
│   ├── trending.html
│   ├── genres.html
│   ├── profile.html
│   └── news.html

└── static/
    ├── style.css
    └── script.js
```

---

## ⚙ Installation

Install required packages:

```bash
pip install flask requests werkzeug
```

Run the application:

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:5000
```

---

## 🗄 Database

Database Name:

```text
animehub.db
```

### Users Table

Stores:

* Username
* Email
* Password

### Watchlist Table

Stores:

* Anime ID
* Anime Title
* Poster Image
* Rating
* User Watchlist Data

---

## 🎯 Project Goals

The goal of Infinity Anime Hub is to provide anime fans with an easy way to discover anime information while helping developers learn:

* Flask Web Development
* SQLite Database Management
* API Integration
* User Authentication
* Responsive Web Design

---

## 🌟 Future Updates

Planned features:

* Favorites System
* Dark / Light Theme Toggle
* Advanced Search Filters
* Anime Recommendations
* User Reviews
* Community Discussion System
* Admin Dashboard
* Personalized Anime Suggestions

---

## ⚠ Disclaimer

Infinity Anime Hub does not host or stream copyrighted anime episodes.

The website only displays anime information and official trailer content using publicly available anime APIs.

---

## 👨‍💻 Author

I.M.Kumar

---

## ⭐ Version

Version: 3.0

Status: Completed & Active Development
