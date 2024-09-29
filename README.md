# Guide to Building a Serverless Movies API with Azure

This guide outlines the process for building a Serverless Movies API using Azure services, including Azure Functions, Cosmos DB, and Azure Blob Storage. It also highlights how Python can complement this process, particularly for automating deployments and programmatically interacting with Azure services.

## Overview

- **Objective**: Create a Serverless Movies API using Azure services.
- **Technologies Used**: 
  - Azure Functions
  - Azure Cosmos DB
  - Azure Blob Storage
  - Python for automation

---

## 1. Azure SDK for Python

The Azure SDK for Python enables interaction with various Azure services from Python scripts.

- **Installation Notes**:
  - Starting from **Azure SDK 5.0.0**, you can no longer install the entire Azure SDK; only submodules are available.
  - To update `pip`, run:
    ```bash
    python3 -m pip install --upgrade pip
    ```

### 1.1 Python Script Overview

Python can streamline operations that would typically require manual execution via the Azure CLI or Azure Portal.

#### Step 1: Install Azure Library Packages

- Create a `requirements.txt` file with the following contents:

    ```plaintext
    # Provides authentication capabilities using Azure Active Directory credentials
    azure-identity

    # Manages Azure resources through Azure Resource Manager (ARM) API
    azure-mgmt-resource

    # Manages Azure Cosmos DB accounts and related resources
    azure-mgmt-cosmosdb

    # Provides management capabilities for Azure Storage resources (Blobs, Files, Queues, Tables)
    azure-mgmt-storage

    # Interacts with Azure Cosmos DB to perform CRUD operations on documents
    azure-cosmos

    # Manages Azure Blob Storage for uploading, downloading, and handling blobs
    azure-storage-blob

    # Develops and manages Azure Functions for serverless computing
    azure-functions

    # Interacts with OpenAI's API for accessing models like GPT-3 and DALL-E (version 0.28)
    openai==0.28

    # Loads environment variables from a .env file for configuration management
    python-dotenv
    ```

- In your terminal or command prompt (with the virtual environment activated), install the requirements:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

#### Step 2: Create a Virtual Environment

To create local environments in VS Code:

1. Open the Command Palette and search for **"Python: Create Environment."**
2. Select the desired interpreter or Python version and the requirements file.
3. A notification will show the progress of the environment creation in your workspace.
4. When prompted, select the new virtual environment for your workspace.

For more details, refer to: [Using Python Environments in Visual Studio Code](#)

#### Step 3: Configure Python Path in VS Code

1. The modules you add may not be recognized by VS Code if they are added to an unrecognized path.
2. Open a terminal and run:
    ```bash
    which python3
    ```
3. Copy the output.
4. In VS Code, go to **Preferences > Settings**, search for **"python.defaultInterpreterPath,"** and paste the path.

#### Step 4: Log in to Azure

1. Access the terminal in VS Code and run:
    ```bash
    az login
    ```
   This allows the Python code to deploy resources to Azure.
   
2. Open the Command Palette in VS Code and type **"Azure sign in."** Log in with your Azure account.
3. Select your subscription in the Azure tab to upload function apps through VS Code.

---

## 2. Create Your Cloud Infrastructure Using Python

### Step 5: Implementation Files

#### 5.1 `main.py`

```python
# Import necessary libraries
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.cosmos import CosmosClient, PartitionKey
from azure.mgmt.storage import StorageManagementClient
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import os

# Load environment variables
load_dotenv()

# Acquire credentials
credential = DefaultAzureCredential()
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
location = 'West Europe'

# Define resource names
resource_group_name = os.environ.get("RG_NAME")
cosmos_account_name = os.environ.get("COSMOS_ACCOUNT")
cosmos_db_name = os.environ.get("COSMOS_DB_NAME")
cosmos_db_container_name = os.environ.get("COSMOS_CONTAINER_NAME")
storage_account_name = os.environ.get("SA_NAME")
storage_account_container_name = os.environ.get("SA_CONTAINER_NAME")
poster_folder = os.environ.get("POSTER_LOCATION")
```

#### 5.2 `resource_group.py`

```python
# Import the main module
import main

# Manage Azure Resource Groups
resource_client = main.ResourceManagementClient(main.credential, main.subscription_id)
resource_group_params = {
    "location": main.location,
    "tags": {
        "Budget": "0€",
        "End date": "Never",
        "Owner": "Alexandre Pereira",
        "Secondary Owner": "None",
        "Team name": "None"
    }
}

# Create the Resource Group
resource_group = resource_client.resource_groups.create_or_update(main.resource_group_name, resource_group_params)
print(f"Provisioned Resource Group {resource_group.name} in the {resource_group.location} region.")
```

#### 5.3 `movies_data.py`

```python
# Import main module
import main

# Define sample movie data
movies = [
    {
        "id": "inception-2010",
        "title": "Inception",
        "releaseYear": "2010",
        "genre": "Science Fiction, Action",
        "coverUrl": f"https://{main.storage_account_name}.blob.core.windows.net/{main.storage_account_container_name}/inception.jpg"
    },
    {
        "id": "shrek-2001",
        "title": "Shrek",
        "releaseYear": "2001",
        "genre": "Comedy, Fantasy",
        "coverUrl": f"https://{main.storage_account_name}.blob.core.windows.net/{main.storage_account_container_name}/shrek.jpg"
    },
    {
        "id": "avengers-2012",
        "title": "Avengers",
        "releaseYear": "2012",
        "genre": "Action, Adventure",
        "coverUrl": f"https://{main.storage_account_name}.blob.core.windows.net/{main.storage_account_container_name}/avengers.jpg"
    }
]
```

#### 5.4 `cosmos_db.py`

```python
# Import necessary modules
import main
import movies_data

# Manage Cosmos DB accounts
cosmos_client = main.CosmosDBManagementClient(main.credential, main.subscription_id)

# Define Cosmos DB account parameters
cosmos_db_params = {
    'location': main.location,
    'locations': [{'location_name': main.location}],
    'kind': 'GlobalDocumentDB',
    'database_account_offer_type': 'Standard'
}

# Provision the Cosmos DB account
cosmos_account = cosmos_client.database_accounts.begin_create_or_update(main.resource_group_name, main.cosmos_account_name, cosmos_db_params).result()
print(f"Provisioned CosmosDB {cosmos_account.name} in the Resource Group {main.resource_group_name} in the {cosmos_account.location} region.")

# Connect to the Cosmos DB SQL account
cosmos_db_uri = cosmos_account.document_endpoint
cosmos_db_primary_key = cosmos_client.database_accounts.list_keys(main.resource_group_name, main.cosmos_account_name).primary_master_key
cosmos_sql_client = main.CosmosClient(cosmos_db_uri, cosmos_db_primary_key)

# Create the Cosmos DB database
database = cosmos_sql_client.create_database_if_not_exists(id=main.cosmos_db_name)
print(f"Provisioned Cosmos DB SQL database '{main.cosmos_db_name}'.")

# Define the container properties and provision the container
partition_key_path = main.PartitionKey(path="/id")
container = database.create_container_if_not_exists(id=main.cosmos_db_container_name, partition_key=partition_key_path, offer_throughput=400)
print(f"Provisioned Cosmos DB container '{main.cosmos_db_container_name}' in the SQL database '{main.cosmos_db_name}' with throughput of 400 RUs.")

# Upsert movie data into Cosmos DB
for movie in movies_data.movies:
    container.upsert_item(movie)
    print(f"Inserted movie data for '{movie['title']}' into the Cosmos DB.")
```

#### 5.5 `storage_account.py`

```python
# Import necessary modules
import main

# Manage Azure Storage accounts
storage_client = main.StorageManagementClient(main.credential, main.subscription_id)

# Define Azure Blob Storage account parameters
storage_account_params = {
    'sku': {'name': 'Standard_LRS'},
    'kind': 'StorageV2',
    'location': main.location,
    'enable_https_traffic_only': True,
    'allow_blob_public_access': True
}

# Provision the Azure Blob Storage account
storage_account = storage_client.storage_accounts.begin_create(main.resource_group_name, main.storage_account_name, storage_account_params).result()
print(f"Provisioned Storage Account {main.storage_account_name} in the Resource Group {main.resource_group_name} in the {storage_account.location} region.")

# Build the blob service client
storage_account_url = f"https://{main.storage_account_name}.blob.core.windows

.net"
blob_service_client = main.BlobServiceClient(account_url=storage_account_url, credential=main.credential)

# Create the container
container_client = blob_service_client.create_container(main.storage_account_container_name)
print(f"Provisioned Container '{main.storage_account_container_name}' in Storage Account '{main.storage_account_name}'.")

# Upload movie poster images
for movie in movies_data.movies:
    image_path = f"{main.poster_folder}/{movie['coverUrl'].split('/')[-1]}"
    blob_client = container_client.get_blob_client(movie['coverUrl'].split('/')[-1])
    
    with open(image_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded movie poster for '{movie['title']}' to Blob Storage.")
```

---

Sure! Here’s a continuation of your guide, following the structure you've provided, along with clearer headings, subheadings, and bullet points for better readability.

---

## 2. Create Serverless Functions

### Step 1: Create the Function Python File

Create a new Python file, e.g., `function_app.py`, and include the following code:

```python
import logging  # Import logging module to log information and errors
import json     # Import json module to handle JSON serialization
import os       # Import os module to access environment variables
import openai   # Import OpenAI's GPT for AI summary generation
import azure.functions as func  # Import Azure Functions HTTP request/response classes
from azure.cosmos import CosmosClient, exceptions  # Import Cosmos client and exception handling
from dotenv import load_dotenv  # Import dotenv to be able to get the .env file

# Load environment variables from .env file
load_dotenv()

# Fetch Cosmos DB credentials from environment variables
# These should be set in the Azure portal under "Application Settings" for security purposes
cosmos_endpoint_uri = os.getenv("COSMOS_DB_ENDPOINT")
key = os.getenv("COSMOS_DB_KEY")
database_name = os.getenv("COSMOS_DB_NAME")
container_name = os.getenv("COSMOS_CONTAINER_NAME")

# Ensure that all Cosmos DB credentials are provided
if not all([cosmos_endpoint_uri, key, database_name, container_name]):
    raise ValueError("Cosmos DB credentials are missing from environment variables.")

# Initialize the Azure Functions app with anonymous access
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Define the route for fetching all movies
@app.route(route="movies")
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    """
    Fetch all movie records from a Cosmos DB collection and return them as a JSON response.
    """
    logging.info('Fetching all movies from Cosmos DB.')
    try:
        client = CosmosClient(cosmos_endpoint_uri, key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        # Read all movie items (max 100 for performance)
        movies = list(container.read_all_items(max_item_count=100))
        movies_json = json.dumps(movies)
        
        # Return the movies list as a JSON response
        return func.HttpResponse(movies_json, mimetype="application/json", status_code=200)

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error occurred while fetching data from Cosmos DB: {e}")
        return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
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
        if not release_year:
            return func.HttpResponse("Please provide a valid year", status_code=400)

        # Query to fetch movies by the specified release year
        query = f"SELECT * FROM c WHERE c.releaseYear = '{release_year}'"
        movies = list(container.query_items(query=query, enable_cross_partition_query=True))

        # Return the fetched movies as a JSON response
        return func.HttpResponse(json.dumps(movies), mimetype="application/json", status_code=200)

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return func.HttpResponse("An unexpected error occurred", status_code=500)

# Define the route for generating a movie summary based on the title
@app.route(route="movies/getmoviesummary/{title}")
def get_movies_by_summary(req: func.HttpRequest) -> func.HttpResponse:
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

        for movie in movies:
            # Generate a summary for the movie using OpenAI
            prompt = f"Generate a summary for the movie {movie_title}: {movie['genre']}"
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ])
            
            movie["generatedSummary"] = response['choices'][0]['message']['content'].strip()
            return func.HttpResponse(json.dumps(movie), mimetype="application/json", status_code=200)

    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse("Error fetching data from Cosmos DB", status_code=500)

    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return func.HttpResponse("Error generating movie summary", status_code=500)
```

### Step 2: Configuring Azure & Functions in VSCode

1. **Install Azure Functions Extension**:
    - Open the command palette in VSCode and type:
      ```
      Azure Functions: Install or Update Azure Functions
      ```
    - This installs/updates the Azure Functions capability in VSCode.

2. **Verify Installation**:
    - In the terminal, check if it is correctly installed:
      ```bash
      func --version
      ```

3. **Create a New Function**:
    - In VSCode, go to the Azure icon in the sidebar, select the Functions icon, and click on **Create Function**.
    - Choose the folder where you want to create the function and select **Python** as the language, and **HTTP trigger** as the template with **Anonymous** access level.
    - The newly created functions will be housed in `function_app.py`.

4. **Configure `local.settings.json`**:
    - Update `local.settings.json` with the following content:
    ```json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python"
      }
    }
    ```

5. **Run in Debug Mode**:
    - In VSCode, click the Azure icon on the sidebar, navigate to your local project, and run in **Debug Mode**.
    - This allows the Azure Functions to recognize the Python functions.

6. **Create Function App in Azure**:
    - Right-click on **Function App** under the Azure icon in the sidebar, then select **Create Function (Advanced)**.
    - Provide the necessary information for the Resource Group created previously and set it to **Consumption based**.
    - This action will create an **App Service Plan** and a **Function App**.

7. **Modify `.funcignore` File**:
    - Update the `.funcignore` file to specify which files and folders to ignore during deployment. This helps avoid uploading unnecessary files.

8. **Deploy to Azure**:
    - To upload the Python functions to the Function App, navigate to the Azure icon in the sidebar, select **Workspace**, then the function icon, and click on **Deploy to Azure**.
    - Select the appropriate **Function App** to deploy to.

---

## 3. GitHub Information

- **Version Control**:
    - Once your application is set up and working locally, register the files and this guide in your Git repository.
    - Use the following commands to initialize a new git repository, stage your files, and commit them:
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Serverless Movies API"
    ```

- **Push to GitHub**:
    - Link your local repository to a remote GitHub repository and push your code:
    ```bash
    git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
    git push -u origin main
    ```
