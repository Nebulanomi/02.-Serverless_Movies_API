import logging
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions

# Cosmos DB connection settings
endpoint = "<COSMOS_DB_ENDPOINT>"
key = "<COSMOS_DB_KEY>"
database_name = 'db_movies'
container_name = 'c_movies-collection'

# Initialize Cosmos client
client = CosmosClient(endpoint, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching all movies from Cosmos DB.')
    
    try:
        # Query to fetch all movies
        movies = list(container.read_all_items())
        
        # Return movies as a JSON response
        return func.HttpResponse(
            json.dumps(movies),
            mimetype="application/json",
            status_code=200
        )
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)