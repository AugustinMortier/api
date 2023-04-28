"""
API for reading Aerosol Alerts Service evaluation database
"""

from enum import Enum
from pathlib import Path
from typing import Union

import polars as pl
import sqlite3
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.utils import *

BASE_DIR = Path("data")

app = FastAPI(
    title="Aerosol Alerts Service API",
    version="0.1.0",
    contact={
        "name": "Augustin Mortier",
        "email": "augustinm@met.no"
    },
    description="Aerosol Alerts Service API for reading the Evaluation Database",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    #root_path="/api/0.1.0" #comment this line when run locally
)

app.add_middleware(GZipMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aerosol-alerts.atmosphere.copernicus.eu","http://localhost:8000","http://127.0.0.1:8000/"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)



@app.get("/")
async def root(request: Request):
    return {
        "title": "Aerosol Alerts Service API",
        "description": "reads evaluation database of the Aerosol Alerts Service and returns results as json files to be visualized in https://aerosol-alerts.atmosphere.copernicus.eu/evaluation.php",
        "status": "OK",
        "root_path": request.scope.get("root_path")
    }


@app.get("/map/{variable}/{network}/{region}")
async def map(
    variable: str = Path(title="Variable", description="Variable (e.g.: od550aer)"),
    network: str = Path(title="Network", description="Observation Network (e.g.: AERONET_V3_Level15)"),
    region: str = Path(title="region", description="region (e.g.: ALL)")
):
    """
    Get list of stations for a given variable, model, and region.
    """

    # connect to database
    DATABASE_URL = Path(BASE_DIR) / "alerts.sqlite"
    get_stations = f"""SELECT station FROM regions WHERE var = '{variable}' AND network = '{network}' AND region = '{region}'"""
    stations = pl.read_database(query=get_stations, connection_uri=f"sqlite://{DATABASE_URL}")

    # get time series of selected stations
    results = []
    for station in stations.rows():
        get_coordinates  = f"""SELECT latitude, longitude FROM coordinates WHERE station = '{station[0]}' AND var = '{variable}' AND network = '{network}'"""
        coordinates = pl.read_database(query=get_coordinates, connection_uri=f"sqlite://{DATABASE_URL}")

        results.append({
            "station_name": station[0],
            "latitude": coordinates['latitude'][0],
            "longitude": coordinates['longitude'][0],
        })

    return results

@app.get("/timeseries/{variable}/{network}/{model}/{region}/{years}/{season}")
async def timeseries(
    variable: str = Path(title="Variable", description="Variable (e.g.: od550aer)"),
    network: str = Path(title="Network", description="Observation Network (e.g.: AERONET_V3_Level15)"),
    model: str = Path(title="Model", description="Model (e.g.: cIFS-12UTC_o-suite)"),
    region: str = Path(title="region", description="region (e.g.: ALL)"),
    years: str = Path(title="years", description="years (e.g.: 2022-2023)"),
    season: str = Path(title="season", description="season (e.g.: ALL)"),
):
    """
    Get time series for a given variable, model, region and time period.
    """

    # connect to database
    DATABASE_URL = Path(BASE_DIR) / "alerts.sqlite"
    connection = sqlite3.connect(DATABASE_URL)

    # create cursor
    cursor = connection.cursor()

    # get list of stations in region for variable
    get_stations = """SELECT station FROM regions WHERE var = ? AND network = ? AND region = ?"""
    params = (variable, network, region)
    stations = cursor.execute(get_stations, params).fetchall()

    # get time series of selected stations
    results = []
    for station in stations:



        results.append({
            "station_name": station[0],
            "latitude": coordinates[0][0],
            "longitude": coordinates[0][1],
        })
    
    # close connection
    connection.close()

    return results

@app.get("/table/{variable}/{network}/{model}/{region}/{years}/{season}")
async def table(
    variable: str = Path(title="Variable", description="Variable (e.g.: od550aer)"),
    network: str = Path(title="Network", description="Observation Network (e.g.: AERONET_V3_Level15)"),
    model: str = Path(title="Model", description="Model (e.g.: cIFS-12UTC_o-suite)"),
    region: str = Path(title="region", description="region (e.g.: ALL)"),
    years: str = Path(title="years", description="years (e.g.: 2022-2023)"),
    season: str = Path(title="season", description="season (e.g.: ALL)"),
):
    """
    Get contingency table for a given variable, model, region and time period.
    """

    results = []

    return results