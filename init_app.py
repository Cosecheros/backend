from fastapi import FastAPI
from api.api import api_router
from fastapi.templating import Jinja2Templates
# import firebase_admin
# from firebase_admin import credentials, firestore

# cred_object = firebase_admin.credentials.Certificate('cosecheros-firebase-adminsdk-5vc3f-6b86b3b3a6.json')
# firebase_admin.initialize_app(cred_object)

app = FastAPI()
app.include_router(api_router)
templates = Jinja2Templates(directory="templates")