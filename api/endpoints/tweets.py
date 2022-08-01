from fastapi import APIRouter, Request, Form
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from scripts.tweets import get_flat_tweets
import csv

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/get_tweets")
async def root(request: Request):
    return templates.TemplateResponse('get_tweets.html', {"request": request})

@router.post("/get_tweets")
def get_tweets(request: Request, fecha: str = Form(...)):
    headers = ["fecha", "usuario", "texto", "alias", "lat", "lon"]
    tweets = get_flat_tweets(fecha)

    with open("tweets.csv", mode="w") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in tweets:
            for field in headers:
                if not field in row:
                    row.update({field : "-"})
            writer.writerow(row)
    return FileResponse("tweets.csv")