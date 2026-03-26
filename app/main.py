import random
import fastapi

from fastapi import HTTPException

from app.data import names

app = fastapi.FastAPI()


@app.get("/")
async def health_check():
    return {"status": "server is running"}

@app.get("/generate_name")
async def generate_name(starts_with: str | None = None):
    name_choices = names
    if starts_with:
        name_choices = [name for name in name_choices if name.lower().startswith(starts_with.lower())]
    
    if not name_choices:
        raise HTTPException(status_code=404, detail="name not found")

    random_name = random.choice(name_choices)
    return {"name": random_name}