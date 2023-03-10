import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Setup homepage and list availible routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

#Set up precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create link from Python to DB
    session = Session(engine)
    
    # Query the results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
    most_recent_date=dt.date(2017, 8 ,23)
    year_ago= most_recent_date - dt.timedelta(days=365)
    results= session.query(measurement.prcp, measurement.date).\
    filter(measurement.date <= most_recent_date ).\
    filter(measurement.date >= year_ago).all()
    
    session.close()
    
    #Convert tuples into a dictionary
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)
    
    #Create JOSN list
    return jsonify(all_precipitation)

# Create station route
@app.route("/api/v1.0/stations")
def stations():
    #Create link from Python to DB
    session=Session(engine)
    
    # Query station information from dataset
    results= session.query(station.id, station.name, station.latitude, station.longitude).all()
    
    session.close()
    
    #Convert tuples into a dictionary
    all_stations=[]
    for row in results:
        station_dict= {}
        station_dict['id']= row[0]
        station_dict['name'] = row[1]
        station_dict['latitude'] = row[2]
        station_dict['longitude'] = row[3]
        all_stations.append(station_dict)
    
    #Create JSON list
    return jsonify(all_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
    #Create link from Python to DB
    session=Session(engine)
    
    #Create a query that returns the last year of data for the most active station "USC00519281"
    most_recent_date2=dt.date(2017,8,18)
    year_ago2= most_recent_date2 - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date <= most_recent_date2 ).\
        filter(measurement.date >= year_ago2).all()
            
    session.close()
    
    #Convert tuples into a dictionary
    all_tobs=[]
    for date, tobs in results:
        tobs_dict={}
        tobs_dict["date"]= date
        tobs_dict["tobs"]= tobs
        all_tobs.append(tobs_dict)
    
    #Create JSON list
    return jsonify(all_tobs)
    
@app.route("/api/v1.0/start")
def start():
    #Create link from Python to DB
    session=Session(engine)
    
   #Query Min, Max and Average temp between a set start and the rest of the DB
    start_date=dt.date(2014,1,14)
    results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    session.close()

    #Convert tuples into a dictionary
    av_start_temp=[]
    for row in results:
        start_temp_dict={}
        start_temp_dict["Min"]= row[0]
        start_temp_dict["Average"]= row[2]
        start_temp_dict["Max"]=row[1]
        av_start_temp.append(start_temp_dict)
    
    #Create JSON list
    return jsonify(av_start_temp)
    
@app.route("/api/v1.0/start/end")
def end():
    #Create link from Python to DB
    session=Session(engine)
    
   #Query Min, Max and Average temp between a set start and end date
    start_date=dt.date(2014,1,14)
    end_date=dt.date(2017,1,14)
    results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()
    
    session.close()

    #Convert tuples into a dictionary
    av_start_end_temp=[]
    for row in results:
        end_temp_dict={}
        end_temp_dict["Min"]= row[0]
        end_temp_dict["Average"]= row[2]
        end_temp_dict["Max"]=row[1]
        av_start_end_temp.append(end_temp_dict)
    
    #Create JSON list
    return jsonify(av_start_end_temp)
    
if __name__ == '__main__':
    app.run()
