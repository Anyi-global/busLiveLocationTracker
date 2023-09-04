from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import socket
import psycopg2

app = Flask(__name__)
geolocator = Nominatim(user_agent="my_app")

# PostgreSQL database connection
# conn = psycopg2.connect(
#     host="localhost",
#     database="your_database_name",
#     user="your_username",
#     password="your_password"
# )

# Create a cursor object to execute database queries
# cursor = conn.cursor()

# Create the 'realtime_locations' table if it doesn't exist
# create_table_query = """
# CREATE TABLE IF NOT EXISTS realtime_locations (
#     id SERIAL PRIMARY KEY,
#     latitude FLOAT,
#     longitude FLOAT
# );
# """
# cursor.execute(create_table_query)
# conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

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
            return render_template('index.html', latitude=latitude, longitude=longitude)
        else:
            return "Address not found."
    except GeocoderTimedOut:
        return "Geocoding service timed out. Please try again later."

@app.route('/vehicle')
def vehicle():
    # Fetch vehicle data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the vehicle.html template and pass the data to it
    return render_template('vehicle.html')

@app.route('/driver')
def driver():
    # Fetch driver data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the driver.html template and pass the data to it
    return render_template('drivers.html')

@app.route('/routes')
def routes():
    # Fetch route data from the database
    # You can use your preferred database access method here to retrieve the data

    # Render the routes.html template and pass the data to it
    return render_template('routes.html')

# @app.route('/locations')
# def locations():
    # Fetch the locations from the 'realtime_locations' table
    # select_query = "SELECT latitude, longitude FROM realtime_locations;"
    # cursor.execute(select_query)
    # locations_data = cursor.fetchall()

    # return render_template('locations.html', locations=locations_data)

if __name__ == '__main__':
    app.run(debug=True)
