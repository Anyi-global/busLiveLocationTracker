from app import app, mongo
from flask import render_template, request, url_for, redirect, flash, session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask import send_from_directory, abort
from flask_mongoengine import MongoEngine
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import bson.binary
import urllib.request
import os, re
import datetime
from functools import wraps

# app.config = os.urandom(24)

app.config["SECRET_KEY"] = "b'n\x1d\xb1\x8a\xc0Jg\x1d\x08|!F3\x04P\xbf'"

# app.config["MONGODB_SETTINGS"] = {
#     'db': 'SIS',
#     'host': 'localhost',
#     'port': 27017   
# }

# db = MongoEngine()
# db.init_app(app)

app.config["UPLOAD_FOLDER"] = "D:/CSI FYP Works/Julius's work/Pet finding app/app/static/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["TXT", "DOC", "PNG", "JPG", "JPEG", "GIF"]
app.config["CLIENT_IMAGES"] = "/Users/Anyiglobal/Desktop/MyProject/app/static/img/clients"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server for Gmail
app.config['MAIL_PORT'] = 587  # Port for TLS
app.config['MAIL_USERNAME'] = 'ikeifeanyi95.ii@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'Skyview95.ii'  # Your Gmail password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

geolocator = Nominatim(user_agent="my_app")

def nigerian_time():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    today = datetime.date.today()
    d2 = today.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S %p")
    return (d2 +' '+'at'+' '+tm)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", 'danger')
            return redirect(url_for("index"))
    return wrap

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You are successfully logged out!", 'success')
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/register")
def register():
    return render_template("public/register.html")

@app.route('/dashboard')
def dashboard():
    return render_template('public/dashboard.html')

@app.route('/geocode', methods=['POST'])
def geocode():
    address = request.form['address']
    try:
        location = geolocator.geocode(address)
        if location is not None:
            latitude = location.latitude
            longitude = location.longitude

            # Insert the latitude and longitude into the 'realtime_locations' table
            # insert_query = "INSERT INTO realtime_locations (latitude, longitude) VALUES (%s, %s);"
            # cursor.execute(insert_query, (latitude, longitude))
            # conn.commit()            
            return render_template('public/dashboard.html', latitude=latitude, longitude=longitude)
        else:
            return "Address not found."
    except GeocoderTimedOut:
        return "Geocoding service timed out. Please try again later."

@app.route('/vehicle')
def vehicle():
    # Fetch vehicle data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the vehicle.html template and pass the data to it
    return render_template('public/vehicle.html')

@app.route('/passenger')
def passenger():
    # Fetch vehicle data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the vehicle.html template and pass the data to it
    return render_template('public/passenger.html')

@app.route('/driver')
def driver():
    # Fetch driver data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the driver.html template and pass the data to it
    return render_template('public/drivers.html')

@app.route('/routes')
def routes():
    # Fetch route data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the routes.html template and pass the data to it
    return render_template('public/routes.html')

# @app.route('/locations')
# def locations():
    # Fetch the locations from the 'realtime_locations' table
    # select_query = "SELECT latitude, longitude FROM realtime_locations;"
    # cursor.execute(select_query)
    # locations_data = cursor.fetchall()

    # return render_template('locations.html', locations=locations_data)

def send_welcome_email(email):
    msg = Message('Welcome to Your App', sender='ikeifeanyi95.ii@gmail.com', recipients=[email])
    msg.body = 'Thank you for creating an account with Your App. We look forward to serving you!'

    mail.send(msg)

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method=='POST':
        req = request.form
        
        username = str(req["username"])
        email = str(req["email"]).lower()
        password = req["pswd"]
        con_password = req["con_pswd"]
        
        # matric_number = mat_no.split('/')
        
        if password != con_password:
            flash("Password Confirmation Mismatched, Please Confirm Your Password!", "danger")
            return render_template("public/register.html")
        # checkuser = mongo.db.sign_up.find_one({"matric_number":mat_no}, {"_id":0})
        checkuser = mongo.db.signup.find_one({username:{"$exists":True}}, {"_id":0})
        if checkuser:
            flash("Sorry, User already registered!", "danger")
            return render_template("public/register.html")
        # checkemail = mongo.db.sign_up.find_one({"email":email}, {"_id":0})
        checkemail = mongo.db.signup.find_one({email:{"$exists":True}}, {"_id":0})
        if checkemail:
            flash("Sorry, User with email address already exists!", "danger")
            return render_template("public/register.html")
        
        mongo.db.signup.insert_one({"username": username, username:username, "email": email, email:email, "password": password, "registeredDate": nigerian_time()})
        send_welcome_email(email)
        flash("Account Created Successfully!", "success")
        return redirect(url_for("index"))
    else:
        return render_template("public/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='POST':
        req = request.form
        
        username = str(req["username"])
        pswd = req["pswd"]
        
        # checkuser = mongo.db.sign_up.find_one({"matric_number": mat_no})
        checkuser = mongo.db.signup.find_one({username:{"$exists":True}}, {"_id":0})
        
        # x = re.search(pattern, string)
        
        if not checkuser:
            flash("Username/Password Incorrect!", "danger")
            return render_template("public/index.html")
        
        elif not pswd == checkuser["password"]:
            flash("Username/Password Incorrect!", "danger")
            return render_template("public/index.html")
                  
        else:
            del checkuser["password"]
            session["user"] = checkuser
            session["login"]=True
            flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
            return redirect(url_for("dashboard"))
    
    return render_template("public/index.html")