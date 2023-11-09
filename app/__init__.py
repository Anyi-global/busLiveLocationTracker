from flask import Flask
from flask_pymongo import PyMongo
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os
import socket
import psycopg2

app = Flask(__name__)


SECRET_KEY = os.environ.get('SECRET_KEY') or "ajajajjsjsjajjajaaw333"

#app configuration
app_settings = os.environ.get(
    'APP_SETTINGS'
    'app.config'
) 
app.config.from_object(app_settings)


#connecting to database
MONGO_URI = "mongodb+srv://fabulous95:Skyview95.ii@cluster0.nz9zg.mongodb.net/BusLiveTracker?retryWrites=true&w=majority"

#initializing PyMongo
mongo = PyMongo(app, MONGO_URI)

from app import views
# from app import admin 
