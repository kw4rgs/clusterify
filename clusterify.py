### L I B R A R I E S ###

import uvicorn
import sys
import pickle
import json
import pandas as pd
import numpy as np
from fastapi import FastAPI, Request, HTTPException, status, Body
from sklearn.neighbors import NearestNeighbors
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import subprocess
from dotenv import load_dotenv
import os

### D O C U M E N T A T I O N ###

description = """
ᴜɴʟᴇᴀꜱʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ᴍᴀᴄʜɪɴᴇ ᴍᴏᴅᴇʟꜱ ᴛᴏ ᴍᴀᴘ ᴀɴᴅ ᴄᴏɴQᴜᴇʀ ᴛʜᴇ ꜱᴄᴀᴛᴛᴇʀᴇᴅ ʀᴇᴀʟᴍꜱ ᴏꜰ ᴅᴀᴛᴀ.

## What you can get:

You can get **clusters, centroids, sets of clustered data**.

## What you can do:

* **Cluterize data** (_not implemented_).
* **Classify data**

## Models:

* K-Means
* K-Means-constrained
* Nearest Neighbors
"""

tags_metadata = [
    {
        "name": "Health Check",
        "description": "Endpoint to check if the server is running",
    },
    {
        "name": "Cluster Centroids",
        "description": "Endpoint to get the number of centroids and their coordinates",
    },
    {
        "name": "Cluster Information",
        "description": "Endpoint to get the customers clustered information",
    },
    {
        "name": "Classify Customers",
        "description": "Endpoint to classify customers to their nearest centroid",
    },
]

# Create a FastAPI app instance
app = FastAPI(    
    title="🅲🅻🆄🆂🆃🅴🆁🅸🅵🆈",
    description=description,
    version="v1.0.0"
    )

load_dotenv()

class CustomerData(BaseModel):
    customer_code: int
    lat: float
    lon: float
    
### A P P L I C A T I O N ###

# Setting up the models and information:

# Path to the uploaded model file
model_file_path = "trained_models/model_trained.pkl"

# Path to the JSON file
json_file_path = "assets/geo_clientes.json"

# Load the model from the file
with open(model_file_path, 'rb') as file:
    loaded_model = pickle.load(file)

# Fit a NearestNeighbors model to the cluster centers
neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(loaded_model.cluster_centers_)

# Define a route to check the health of the server
@app.get("/",  tags=["Health Check"])
async def check_health():
    
    env = os.getenv("ENVIRONMENT")
    
    try:
        output = subprocess.check_output("uptime", shell=True).decode("utf-8")
        uptime = output.split("up ")[1].split(",")[0].strip()
        pass
    except Exception as e:
        # If the check fails, raise an HTTPException with a 500 error code and the error message
        raise HTTPException(status_code=500, detail=str(e))

    # If the check succeeds, return a JSON response with some status information
    return {
        "service": "█▓▒▒░░░ Clusterify ░░░▒▒▓█",
        "message": "The heartbeat of our server is strong and steady.",
        "status": "up",
        "uptime": uptime,
        "details": {
            "name": "Clusterify",
            "version": "1.0.0",
            "environment": env,
        }
    }

# Get the current centroids and model clusterized information to work with
@app.get("/api/v1/cluster_centers", tags=["Cluster Centroids"])
def get_cluster_centers():
    try:
        # Get the cluster centers and their indices
        cluster_centers = loaded_model.cluster_centers_
        indices = range(len(cluster_centers))

        # Create a dictionary with cluster centers and indices
        data = {
            'clusters': [{
                'cluster': i, 
                'centroid': {
                    'lat': center[0], 
                    'lon': center[1] 
                }} 
        for i, center in zip(indices, cluster_centers)]}

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred while retrieving cluster centers")

# Get the current model data with the customers
@app.get("/api/v1/clustered_data", tags=["Cluster Information"])
def get_clustered_data():
    try:
        # Load JSON data from the file
        with open(json_file_path) as file:
            json_data = file.read()

        # Load JSON data
        data = json.loads(json_data)

        # Create empty lists for columns
        codigo_cliente = []
        latitud = []
        longitud = []

        # Iterate over the "clientes" list in the JSON data
        for obj in data['clientes']:
            codigo_cliente.append(obj['cliente']['codigo'])
            latitud.append(float(obj['cliente']['geolocalizacion']['latitud']))
            longitud.append(float(obj['cliente']['geolocalizacion']['longitud']))

        # Create a dataframe from the extracted columns
        df = pd.DataFrame({
            'codigo_cliente': codigo_cliente,
            'lat': latitud,
            'long': longitud
        })

        # Remove unnecessary columns
        train_df = df.drop(columns=['codigo_cliente'])

        # Perform clustering
        train_df['cluster'] = pd.Series(loaded_model.predict(train_df), index=train_df.index)
        train_df['codigo_cliente'] = df['codigo_cliente']

        # Convert clustered data to JSON
        clustered_data = train_df.to_dict(orient='records')
        
        # Formatting the data
        clusters = {}

        # Iterate over the clustered data
        for item in clustered_data:
            cluster = item['cluster']
            customer_code = item['codigo_cliente']
            lat = float(item['lat'])
            lon = float(item['long'])

            if cluster in clusters:
                clusters[cluster]['customers'].append({
                    'customer_code': customer_code,
                    'coordinates': {
                        'lat': lat,
                        'long': lon
                    }
                })
            else:
                clusters[cluster] = {
                    'cluster': cluster,
                    'customers': [{
                        'customer_code': customer_code,
                        'coordinates': {
                            'lat': lat,
                            'long': lon
                        }
                    }]
                }

        # Create the final data dictionary
        cluster_set = {'cluster_set': list(clusters.values())}
        
        sorted_data = sorted(cluster_set['cluster_set'], key=lambda x: x["cluster"])
        cluster_set["cluster_set"] = sorted_data
        return cluster_set

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON data")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/classify_customers", tags=["Classify Customers"])
async def classify_customers(request: Request, body: List[CustomerData] = Body(...)):
    """
    Nearest neighbor classification model to classify customers.

    - **customer_code**: Integer representing the customer code.
    - **lat**: Float representing the latitude.
    - **lon**: Float representing the longitude.
    """
    try:
        # Extract the JSON payload from the request body
        payload = await request.json()

        # Validate payload
        if not isinstance(payload, list):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload format")

        classified = []

        for item in payload:
            try:
                # Validate and extract the values from each item in the payload
                codigo_cliente = int(item['customer_code'])
                lat = float(item['lat'])
                lon = float(item['lon'])
            except (KeyError, ValueError):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid item format")

            # Calculate the distances from the new data point to the cluster centers
            distances, indices = neigh.kneighbors([[lat, lon]])

            # Get the index of the cluster with the minimum distance
            nearest_cluster = indices[0][0]

            # Assign the predicted cluster to the new codigo_cliente
            nearest_cluster_cliente = int(nearest_cluster)

            # Create the customer dictionary
            customer_data = {
                "customer_code": codigo_cliente,
                "coordinates": {
                    "lat": lat,
                    "lon": lon
                },
                "nearest_cluster": nearest_cluster_cliente
            }

            # Append the customer data to the list
            classified.append(customer_data)

        # Formatting
        formatted_output = {"classified": []}

        for item in classified:
            nearest_cluster = item["nearest_cluster"]
            customer_code = item["customer_code"]
            lat = item["coordinates"]["lat"]
            lon = item["coordinates"]["lon"]

            # Check if the nearest_cluster already exists in the formatted output
            cluster_exists = False
            for cluster_item in formatted_output["classified"]:
                if cluster_item["nearest_cluster"] == nearest_cluster:
                    cluster_exists = True
                    cluster_item["customers"].append({
                        "customer_code": customer_code,
                        "coordinates": {"lat": lat, "lon": lon}
                    })
                    break

            # If the nearest_cluster does not exist, create a new entry
            if not cluster_exists:
                formatted_output["classified"].append({
                    "nearest_cluster": nearest_cluster,
                    "customers": [
                        {
                            "customer_code": customer_code,
                            "coordinates": {"lat": lat, "lon": lon}
                        }
                    ]
                })

        sorted_data = sorted(formatted_output["classified"], key=lambda x: x["nearest_cluster"])
        return sorted_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON payload")


# If this file is executed directly, start the server with Uvicorn
if __name__ == "__main__":
    uvicorn.run("clusterify:app", host="127.0.0.1", port=6969, reload=True, workers=4)
