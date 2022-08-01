from fastapi import APIRouter
from scripts import test_firebase

router = APIRouter()

@router.get("/")
async def root():
    test_firebase.testing()
    return {"message": "Hello Fire docs"}