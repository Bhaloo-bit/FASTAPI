import secrets, string
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi .responses import RedirectResponse

from database import create_db_and_tables, SessionDep
from models import URLMapping, URLCreate, URLResponse, Analytics, AnalyticsResponse

BASE_URL = "http://localhost:8000"

ALPHABET = string.ascii_letters + string.digits

def generate_code(length: int=6) -> str:
    "it will generate 6 alphanumeric code"
    return "".join(secrets.choice(ALPHABET) for _ in range(length))

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
# to make call with the db

app = FastAPI(lifespan=lifespan)

# to original url to the db
@app.post("/shorten", response_model=URLResponse)
def shorten(data: URLCreate, session: SessionDep):
    code = generate_code()
    while session.get(URLMapping, code): # avoid collisions
        code = generate_code()

    session.add(URLMapping(short_url=code, original_url = str(data.original_url)))
    session.add(Analytics(short_url=code))
    session.commit()
    return URLResponse(short_url=f"{BASE_URL}/{code}")


# to get analytics form 

@app.get("/analytics/{short_url}", response_model=AnalyticsResponse)
def get_analytics(short_url:str, session: SessionDep):
    stats = session.get(Analytics, short_url)
    if not stats:
        raise HTTPException(status_code=404, detail= "short URL not found")
    return stats

# to get the short url with id
@app.get("/{short_url}")
def redirect(short_url: str, session: SessionDep):
    mapping = session.get(URLMapping, short_url)
    if not mapping:
        raise HTTPException(status_code=404, detail="Short URL not found")

    stats = session.get(Analytics, short_url)
    stats.click_count +=1
    stats.last_accessed = datetime.now(timezone.utc)
    session.add(stats)
    session.commit()
    session.refresh(stats)

    return RedirectResponse(mapping.original_url, status_code=307)