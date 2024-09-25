# Import CosmosClient to interact with Azure Cosmos DB
from azure.cosmos import CosmosClient
from create_resources import storage_account_name

# Import os module to access environment variables
import os

# Step 1: Set up Cosmos DB connection
cosmos_endpoint_uri = os.getenv("COSMOS_DB_ENDPOINT")
key = os.getenv("COSMOS_DB_KEY")

# Step 2: Initialize Cosmos Client
# CosmosClient establishes a session with the Cosmos DB account using the provided endpoint and key.
client = CosmosClient(cosmos_endpoint_uri, key)

# Step 3: Define the database and container names
# A Cosmos DB account contains databases, and each database contains containers.
# Containers are equivalent to a collection of tables where your documents (JSON items) are stored.
database_name = 'db_movies'
container_name = 'c_movies-collection'

# Step 4: Create the database if it doesn't exist
# This creates a database with the specified name, or returns the existing one if it already exists.
database = client.create_database_if_not_exists(id=database_name)

# Step 5: Create the container if it doesn't exist
# 'partition_key' defines the partitioning strategy, which helps scale and optimize queries, it is used to distribute and query the data.
# In this case, the movie title will be used as the partition key.
container = database.create_container_if_not_exists(id=container_name, partition_key="/id")

# Step 6: Define the sample movie data
# This is a JSON-like Python dictionary containing the movie details you want to insert into Cosmos DB.
# 'coverUrl' is the URL to the movie cover image in Blob Storage.
movie_data = {
    "id" : "inception-2010", # Unique identifier for the document
    "title" : "Inception",
    "releaseYear" : "2010",
    "genre" : "Science Fiction, Action",
    "coverUrl" : f"https://{storage_account_name}.blob.core.windows.net/moviecovers/inception.jpg"
}

# Step 7: Insert the movie data into the container
# The 'upsert_item' method inserts the movie_data into the container if it's a new item, or updates the existing item if it already exists (based on the partition key, 'title').
container.upsert_item(movie_data)

# Success message to confirm the operation
print(f"Inserted movie data for '{movie_data['title']}' into the Cosmos DB.")