from threading import active_count
import pandas as pd
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, json, jsonify

##################
# Database Setup
##################

# Create the engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Table reference
Measurement = Base.classes.measurement
Station = Base.classes.station

# Open/create session
session = Session(engine)

##################
# Flask Setup
##################
app = Flask(__name__)

##################
# Flask Routes
##################

# / - home page - list all routes that are available

@app.route("/")
def Home_page():
    """List all available api routes."""
    return (
        f"Welcome to Climate App w/ API<br>"
        f"Listed below are all the available API routes currently available.</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/&lt;start&gt;</br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;</br>"
    )

# /api/v1.0/precipitation - Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
   # Find the most recent date in the data set. (In Measurement)
    result = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    str(result[0]) 

    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    recent_date = dt.datetime.strptime(str(result[0]), '%Y-%m-%d')
    recent_date
    one_year_ago = recent_date - dt.timedelta(days=365)
    one_year_ago

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > one_year_ago).all()



# Convert the query results to a dictionary using date as the key and prcp as the value.
    total_precip = []
    for date, prcp in results:
        if prcp != None:
            precip_dict = {}
            precip_dict[date] = prcp
            total_precip.append(precip_dict)
# Return the JSON representation of your dictionary.
    return jsonify(total_precip)
session.close()



# Create new route to list all Stations

session = Session(engine)   

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    """ Return list of all Stations """
    all_stations = session.query(Station.station).all()

    session.close()

# Covenvert list into dict. 

    station_list = list(np.ravel(all_stations))

    return jsonify(station_list)


# Create new route to list all Stations


# Query the dates and temperature observations of the most active station for the last year of data.

@app.route("/api/v1.0/tobs")
def tobs():
    """Return list of all Stations """
    session = Session(engine)
    one_year_ago = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    result = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= one_year_ago).all()

    session.close()
    

 
    temp_dict= {}
    for temp, date in result:
        if temp != None:
            temp_dict[date] = temp
    return jsonify(temp_dict)


# Start session for next start/end route 



# Create route 
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def temp(start, end = None):
        """Return list of all temperatures"""
        session = Session(engine)
        start_date = session.query(Measurement.tobs, Measurement.date, func.min(Measurement.tobs), func.avg (Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date.desc())
        str(start_date[0])
        print(str(start_date[0]))

        session.close()

        start_temp= {}
        for temp, date, min, avg, max in start_date:
            if temp != None:
                start_temp[date] = [temp, min, avg, max]
                
        

        return jsonify(start_temp)

        # (Measurement.tobs, func.min(Measurement.tobs), func.avg (Measurement.tobs), func.max(Measurement.tobs))










if __name__ == '__main__':
    app.run()