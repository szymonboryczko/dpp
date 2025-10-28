from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from contextlib import asynccontextmanager
import csv
import os

app = FastAPI()


# konfiguracja bazy

DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



#modele orm

class Movie(Base):
    __tablename__ = "movies"
    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genres = Column(String)


class Link(Base):
    __tablename__ = "links"
    movieId = Column(Integer, primary_key=True, index=True)
    imdbId = Column(String)
    tmdbId = Column(String)


class Rating(Base):
    __tablename__ = "ratings"
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer, primary_key=True)
    rating = Column(Float)
    timestamp = Column(Integer)


class Tag(Base):
    __tablename__ = "tags"
    userId = Column(Integer, primary_key=True)
    movieId = Column(Integer)
    tag = Column(String)
    timestamp = Column(Integer)



# stworzenie bazy danych

if not os.path.exists("./movies.db"):
    Base.metadata.create_all(bind=engine)
    print("📦 Utworzono bazę danych (movies.db).")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ładowanie plików csv do bazy danych

def load_data_if_empty(db: Session):
    movie_count = db.query(Movie).count()
    if movie_count == 0:
        print("📥 Ładowanie danych z CSV do bazy...")

        base_path = "C:/Users/Sz/UE/2 stopień/dpp reszta"

        # Movies
        with open(f"{base_path}/movies.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.add(Movie(movieId=int(row["movieId"]), title=row["title"], genres=row["genres"]))
        db.commit()

        # Links
        with open(f"{base_path}/links.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.add(Link(movieId=int(row["movieId"]), imdbId=row["imdbId"], tmdbId=row["tmdbId"]))
        db.commit()

        # Ratings
        with open(f"{base_path}/ratings.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.add(Rating(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"])
                ))
        db.commit()

        # Tags
        with open(f"{base_path}/tags.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.add(Tag(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    tag=row["tag"],
                    timestamp=int(row["timestamp"])
                ))
        db.commit()

        print("✅ Dane zostały załadowane do bazy.")
    else:
        print("✅ Dane już są w bazie, pomijam ładowanie.")


#endpointy
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    load_data_if_empty(db)
    db.close()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()


@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    return db.query(Link).all()


@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@app.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()
