# Guide:

This guide outlines how to build a Serverless Movies API using Azure services, such as Azure Functions, Cosmos DB, and Azure Blob Storage.
Below, I'll describe how Python might be used to complement this process, specifically for tasks like automating deployments or interacting with Azure services programmatically. 

## 1. Azure SDK for Python:

The Azure SDK for Python (azure · PyPI) can be used to interact with Azure services such as Cosmos DB, Blob Storage, and Azure Functions from Python scripts.
Starting from "Azure 5.0.0" we can't install the entirel azure SDK anymore, only sub modules.
To update pip, run: python3 -m pip install --upgrade pip

Here’s how Python can help with each step in the process, automating some of the operations you would otherwise execute manually via the Azure CLI or Azure Portal.

### Step 1 (Create a virtual environment):

To create local environments in VS Code using virtual environments or Anaconda, you can follow these steps: open the Command Palette (⇧⌘P), search for the "Python: Create Environment" command, and select it.
If you are creating an environment using Venv, the command presents a list of interpreters that can be used as a base for the new virtual environment.
After selecting the desired interpreter or Python version, a notification will show the progress of the environment creation and the environment folder will appear in your workspace.
When you create a new virtual environment, a prompt will be displayed in VS Code to allow you to select it for the workspace, we say yes.

We will then have the below:

![image](https://github.com/user-attachments/assets/4a7d2da5-6f55-46b3-936b-edc4b92d4255)

Link: Using Python Environments in Visual Studio Code

### Step 2 (Install the Azure library packages):

Create a file named requirements.txt with the following contents:

azure-identity
azure-mgmt-resource
azure-mgmt-cosmosdb
azure-mgmt-storage

azure-cosmos
azure-storage-blob
azure-functions

openai ==0.28

We can use the first 4 libraries to automate the identity initialization and to manage resource groups, storage accounts, and Cosmos DBs.
The other three are used to manage the client of a cosmosdb along with its data and to manage data for a blob storage and functions.
The last one is used to interact with na older version of OpenAI.

In a terminal or command prompt with the virtual environment activated, install the requirements: python3 -m pip install -r requirements.txt

### Step 3 (Add python path to VScode):

The modules we are adding could possibly not be used by Vscode since they are being added to a path that it doesnt recognize.
To fix this on my side I added the python3 path to Vscode.
To do so I went to a terminal and typed: which python3
We then copied the output and went to vs code -> Preferences -> Settings -> Typed in "python.defaultInterpreterPath" and added the previous path to the box.
Vscode will now understand the modules that were added.

### Step 4 (Create Your Cloud Infrastructure Using Python):

	# Import the needed credential and management objects from the libraries
	import os
	from azure.identity import DefaultAzureCredential
	from azure.mgmt.resource import ResourceManagementClient
	from azure.mgmt.cosmosdb import CosmosDBManagementClient
	from azure.mgmt.storage import StorageManagementClient
 
	Step 1: Acquire credentials
	# DefaultAzureCredential automatically attempts to authenticate using various methods, such as:
	# - Environment variables (like AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
	# - Azure Managed Identity if running in an Azure environment
	# - Visual Studio or Azure CLI authentication for local development
	credential = DefaultAzureCredential()
 
	# Step 2: Define subscription ID and location
	# Retrieve the Azure Subscription ID from the environment variable, or use a hardcoded fallback.
	# This subscription ID is required to authenticate the API requests.
	subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
	# The region where we want to create the resources
	location = 'West Europe'
 
	# Step 3: Obtain a client for managing Azure Resource Groups
	# ResourceManagementClient allows us to interact with Azure Resource Groups.
	resource_client = ResourceManagementClient(credential, subscription_id)
 
	# Step 4: Define the Resource Group parameters
	resource_group_name = 'rg-movies_api_resource_group'
	resource_group_params = {
	"location": location,
	"tags": {
	"Budget": "0€",
	"End date": "Never",
	"Owner" : "Alexandre Pereira",
	"Secondary Owner" : "None",
	"Team name" : "None"
	}
	}
 
	# Step 5: Create the Resource Group
	# This API call creates or updates a resource group in the specified region.
	resource_group = resource_client.resource_groups.create_or_update(resource_group_name, resource_group_params)
	print(f"Provisioned Resource Group {resource_group.name} in the {resource_group.location} region.")
 
	# Step 6: Obtain a client for managing Cosmos DB accounts
	# CosmosDBManagementClient lets you manage CosmosDB accounts, databases, and collections.
	cosmos_client = CosmosDBManagementClient(credential, subscription_id)
 
	# Step 7: Define Cosmos DB account parameters
	# A Cosmos DB account is a globally distributed, multi-model database service.
	cosmos_db_name = 'db-moviescosmosdb'
	cosmos_db_params = {
	'location': location,
	'locations': [{'location_name': location}],  # Specifies the location where the data is stored
	'kind': 'GlobalDocumentDB',  # Database type (GlobalDocumentDB is for the SQL API, Cosmos DB's default)
	'database_account_offer_type': 'Standard'  # Offer type (Standard is the default pricing tier)
	}
 
	# Step 8: Provision the Cosmos DB account
	# This operation is asynchronous, so we wait for it to complete with .result().
	# We are creating or updating the Cosmos DB account with the provided parameters.
	cosmos_db = cosmos_client.database_accounts.begin_create_or_update(resource_group_name, cosmos_db_name, cosmos_db_params).result()
	print(f"Provisioned CosmosDB {cosmos_db.name} in the Resource Group {resource_group.name} in the {cosmos_db.location} region.")
 
	# Step 9: Obtain a client for managing Azure Storage accounts
	# StorageManagementClient lets you manage Azure Storage accounts (Blob, File, Table, Queue).
	storage_client = StorageManagementClient(credential, subscription_id)
 
	# Step 10: Define Azure Blob Storage account parameters
	storage_account_name = 'samoviescoverstorage'
	storage_account_params = {
	'sku': {'name': 'Standard_LRS'},
	'kind': 'StorageV2',
	'location': location
	}
	### Add the creation of a container here
 
	# Step 11: Provision the Azure Blob Storage account
	# Like CosmosDB, creating a storage account is an asynchronous operation, so we wait for completion with .result().
	storage_account = storage_client.storage_accounts.begin_create(resource_group_name, storage_account_name, storage_account_params).result()
	print(f"Provisioned Storage Account {storage_account.name} in the Resource Group {resource_group.name} in the {storage_account.location} region.")

### Step 5 (.env file):

Now we create a .env file to add the environment variable values:

	# Example for local settings in the `.env` file
	AZURE_SUBSCRIPTION_ID = "e9fe39b1-4bf8-4963-8d1c-b8ea2f1606b1"
	COSMOS_DB_ENDPOINT = "https://db-moviescosmosdb.documents.azure.com:443/"
	COSMOS_DB_KEY = "key"
	COSMOS_DB_NAME = "db_movies"
	COSMOS_CONTAINER_NAME = "c_movies-collection"
	SAS_CONNECTION_STRING = 
	"BlobEndpoint=https://samoviescoverstorage.blob.core.windows.net/;
	QueueEndpoint=https://samoviescoverstorage.queue.core.windows.net/;
	FileEndpoint=https://samoviescoverstorage.file.core.windows.net/;
	TableEndpoint=https://samoviescoverstorage.table.core.windows.net/;
	SharedAccessSignature=sv=2022-11-02&ss=b&srt=sco&sp=rwdlaciytfx&se=2024-09-25T17:10:25Z&st=2024-09-25T09:10:25Z&spr=https&sig=2BY6KxxCEKCWY%2F%2FyYooALaR4BSLARMCW%2FUEJ0HYWC68%3D"
	OPENAI_KEY = "---"

### Step 6 (Run the script to test):

Sign in to Azure using the Azure CLI: az login

Set the AZURE_SUBSCRIPTION_ID environment variable to your subscription ID: set AZURE_SUBSCRIPTION_ID=00000000-0000-0000-0000-000000000000
You can run the following command and get your subscription ID from the id property in the output: az account show

Run the script: python3 file_name.py

## 2. Prepare Your Data with Python:

You can use Python to upload movie data to Azure Cosmos DB and Blob Storage. 

### Step 1 (Sample Python code to upload a movie cover to Blob Storage):

	# Import BlobServiceClient to interact with Azure Blob Storage
	from azure.storage.blob import BlobServiceClient
	# Import os module to access environment variables
	import os
	# Step 1: Set up Blob Storage connection
	sas_connection_string = os.getenv("SAS_CONNECTION_STRING")
	# Step 2: Initialize BlobServiceClient
	# BlobServiceClient allows interaction with Blob storage services using the provided connection string.
	blob_service_client = BlobServiceClient.from_connection_string(sas_connection_string)
	# Step 3: Define the container and blob (file) details
	container_name = 'moviecovers'
	blob_name = 'inception.jpg'
	# Step 4: Create a BlobClient
	# BlobClient is used to upload or download blobs (files).
	blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
	# Step 5: Upload the local image file to Blob Storage
	# Uploads the image file in binary mode ('rb' stands for read binary).
	with open("movies/inception.jpg", "rb") as data:
	blob_client.upload_blob(data)
	# Success message to confirm the operation
	print(f"Uploaded movie cover '{blob_name}' to Blob Storage in container '{container_name}'.")

### Step 2 (Sample Python code to upload movie data to Cosmos DB):

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

## 3. Create Serverless Functions:

### Step 1 (Create the function python file):

	import logging  # Import logging module to log information and errors
	import json     # Import json module to handle JSON serialization
	import os       # Import os module to access environment variables
	import openai   # Import OpenAI's GPT for AI summary generation
 
	import azure.functions as func  # Import Azure Functions HTTP request/response classes
	from azure.cosmos import CosmosClient, exceptions  # Import Cosmos client and exception handling
 
	# Fetch Cosmos DB credentials from environment variables
	# These should be set in the Azure portal under "Application Settings" for security purposes
	cosmos_endpoint_uri = os.getenv("COSMOS_DB_ENDPOINT")
	key = os.getenv("COSMOS_DB_KEY")
	database_name = os.getenv("COSMOS_DB_NAME")
	container_name = os.getenv("COSMOS_CONTAINER_NAME")
 
	# Ensure that all Cosmos DB credentials are provided
	# This raises an error if any are missing
	if not all([cosmos_endpoint_uri, key, database_name, container_name]):
	raise ValueError("Cosmos DB credentials are missing from environment variables.")
 
	# Initialize the Azure Functions app with anonymous access
	app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
 
	# Define the route for this function
	# It will be accessed via "/movies" URL
	@app.route(route="movies")
	def get_movies(req: func.HttpRequest) -> func.HttpResponse:
	"""
	This function is triggered by an HTTP request.
	It retrieves all movie records from a Cosmos DB collection and returns them as a JSON response.
	"""
	logging.info('Fetching all movies from Cosmos DB.')
 
	try:
	# Initialize the Cosmos client within the function
	# This ensures the client is only created when needed, improving performance in serverless environments
	client = CosmosClient(cosmos_endpoint_uri, key)
	
	# Get a reference to the specific database and container (collection) where movies are stored
	database = client.get_database_client(database_name)
	container = database.get_container_client(container_name)
	
	# Query the container to read all items (movies) with a maximum item count (100) for better performance
	movies = list(container.read_all_items(max_item_count=100))
	
	# Convert the list of movie objects to JSON format for the HTTP response
	movies_json = json.dumps(movies)
	
	# Return the movies list as a JSON response with a 200 status (success)
	return func.HttpResponse(movies_json, mimetype="application/json", status_code=200)
	
	except exceptions.CosmosHttpResponseError as e:
	# Catch specific Cosmos DB errors and log the error details
	logging.error(f"Error occurred while fetching data from Cosmos DB: {e}")
	
	# Return a 500 (Internal Server Error) response if there's a Cosmos DB issue
	return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)
	
	except Exception as e:
	# Catch any other unexpected errors and log them for troubleshooting
	logging.error(f"Unexpected error: {e}")
	
	# Return a 500 (Internal Server Error) response if any generic error occurs
	return func.HttpResponse("An unexpected error occurred", status_code=500)
 
	# Define the route for fetching movies by release year
	@app.route(route="movies/getmoviesbyyear/{year}")
	def get_movies_by_year(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Fetching movies by release year from Cosmos DB.')
	
	try:
	client = CosmosClient(cosmos_endpoint_uri, key)
	database = client.get_database_client(database_name)
	container = database.get_container_client(container_name)
	
	# Get year from URL parameters
	release_year = req.route_params.get('year')
	
	# Check if a valid year was provided
	if not release_year:
	return func.HttpResponse("Please provide a valid year", status_code=400)
 
	# Construct a query to fetch movies by the specified release year
	query = f"SELECT * FROM c WHERE c.releaseYear = '{release_year}'"
	movies = list(container.query_items(query=query, enable_cross_partition_query=True))
 
	# Return the fetched movies as a JSON response with a 200 status (success)
	return func.HttpResponse(json.dumps(movies), mimetype="application/json", status_code=200)
	
	# Log any errors that occur while fetching from Cosmos DB
	except exceptions.CosmosHttpResponseError as e:
	logging.error(f"Error occurred: {e}")
	return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)
	
	# Log unexpected errors and return a generic error message
	except Exception as e:
	logging.error(f"Unexpected error: {e}")
	return func.HttpResponse("An unexpected error occurred", status_code=500)
 
	# Define the route for generating a movie summary based on the title
	@app.route(route="movies/getmoviesummary/{title}")
	def main(req: func.HttpRequest) -> func.HttpResponse:
	logging.info('Fetching movie details for summary generation.')
	client = CosmosClient(cosmos_endpoint_uri, key)
	database = client.get_database_client(database_name)
	container = database.get_container_client(container_name)
 
	# OpenAI API Key for accessing the AI model
	openai.api_key = os.getenv("OPENAI_KEY")
	movie_title = req.route_params.get('title')
	
	if not movie_title:
	return func.HttpResponse("Please provide a valid movie title", status_code=400)
	try:
	query = f"SELECT * FROM c WHERE c.title = '{movie_title}'"
	movies = list(container.query_items(query=query, enable_cross_partition_query=True))
	
	if not movies:
	return func.HttpResponse(f"Movie with title {movie_title} not found", status_code=404)

 	# Use OpenAI to generate a summary for the movie
	for movie in movies:
	prompt = f"Generate a summary for the movie {movie_title}: {movie['genre']}"
	response = openai.ChatCompletion.create(
	model="gpt-4o-mini",
	messages=[
	{"role": "system", "content": "You are a helpful assistant."},
	{"role": "user", "content": prompt}
	])
	
	movie["generatedSummary"] = response['choices'][0]['message']['content'].strip()
 
	# Return movie data with generated summary
	return func.HttpResponse(json.dumps(movie), mimetype="application/json", status_code=200)
	
	except exceptions.CosmosHttpResponseError as e:
	logging.error(f"Error occurred: {e}")
	return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)
	
	except Exception as e:
	logging.error(f"Error generating summary: {e}")
	return func.HttpResponse("Error generating movie summary", status_code=500)

### Step 2 (Configuring Azure & Functions in VScode):

In Vscode open the command pallete and write "Azure functions: install or update azure functions
This is to install/update the azure function capability in vscode.

We then type the following in a terminal to see if its correctly installed: func --version
Then in Vscode go to the Azure icon on the tab -> functions icon -> Create function
Choose the folder where this is being done and a the new project as Python and httptrigger and anonymous.
Function_app.py is the file that contains the functions.
In local.settings.json, add "AzureWebJobsStorage": "UseDevelopmentStorage=true".
Install Azurite in Vscode and then in the pallet type "Azurite: start"
After its up, run the function python code with f5.
Go to the comand pallet again in vscode and type in "Azire:Sign in"
After that, in the azure icon on the tab, select the subscription we want to use.
Then go to the resources -> function app -> right-click -> create function (advanced).
Then add the information of the RG that has the resources created above.
Have it work with a service plan.

After that, upload the functions we created with python to that function app by right clicking it -> Deploy function.

## 4. GitHub information:

I then register the files and this guide in my git.
