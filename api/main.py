from typing import Union
import csv
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class Movie:
    def __init__(self, movieId: int, title: str, genres: str):
        self.movieId = movieId
        self.title = title
        self.genres = genres

class Link:
    def __init__(self, movieId: int, imdbId: str, tmdbId: str):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId

class Rating:
    def __init__(self, userId: int, movieId: int, rating: float, timestamp: int):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp

class Tag:
    def __init__(self, userId: int, movieId: int, tag: str, timestamp: int):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = timestamp


# 3️⃣ Endpoint /movies
@app.get("/movies")
def get_movies():

    movies = []


    with open("C:/Users/Sz/UE/2 stopień\dpp reszta\movies.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)


        for row in reader:

            movie = Movie(
                movieId=int(row["movieId"]),
                title=row["title"],
                genres=row["genres"]
            )


            movies.append(movie.__dict__)


    return movies

@app.get("/links")
def get_links():
    links = []
    with open("C:/Users/Sz/UE/2 stopień/dpp reszta/links.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = Link(
                movieId=int(row["movieId"]),
                imdbId=row["imdbId"],
                tmdbId=row["tmdbId"]
            )
            links.append(link.__dict__)
    return links


@app.get("/ratings")
def get_ratings():
    ratings = []
    with open("C:/Users/Sz/UE/2 stopień/dpp reszta/ratings.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rating = Rating(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                rating=float(row["rating"]),
                timestamp=int(row["timestamp"])
            )
            ratings.append(rating.__dict__)
    return ratings


@app.get("/tags")
def get_tags():
    tags = []
    with open("C:/Users/Sz/UE/2 stopień/dpp reszta/tags.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = Tag(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                tag=row["tag"],
                timestamp=int(row["timestamp"])
            )
            tags.append(tag.__dict__)
    return tags