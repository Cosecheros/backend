from fastapi import APIRouter, Request
from api.endpoints import tweets, fire_docs
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
api_router = APIRouter()

@api_router.get("/")
async def root(request: Request):
    return templates.TemplateResponse('mainpage.html', {"request": request})

api_router.include_router(fire_docs.router, prefix="/fire_docs", tags=["fire_docs"])
api_router.include_router(tweets.router, prefix="/tweets", tags=["tweets"])