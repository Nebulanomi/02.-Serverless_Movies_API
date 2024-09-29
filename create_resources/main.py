# Import the needed credential and management objects from the libraries
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.cosmos import CosmosClient, PartitionKey
from azure.mgmt.storage import StorageManagementClient
from dotenv import load_dotenv # Import dotenv to be able to get the .env file
from azure.storage.blob import BlobServiceClient

# Take environment variables from .env
load_dotenv()

# Acquire credentials
credential = DefaultAzureCredential()

# DefaultAzureCredential automatically attempts to authenticate using various methods, such as:
    # - Environment variables (like AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)
    # - Azure Managed Identity if running in an Azure environment
    # - Visual Studio or Azure CLI authentication for local development

# Retrieve the Azure Subscription ID from the environment variable
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")

# The region where we want to create the resources
location = 'West Europe'

# Define the resource names
resource_group_name = os.environ.get("RG_NAME")
cosmos_account_name = os.environ.get("COSMOS_ACCOUNT")
cosmos_db_name = os.environ.get("COSMOS_DB_NAME")
cosmos_db_container_name = os.environ.get("COSMOS_CONTAINER_NAME")
storage_account_name = os.environ.get("SA_NAME")
storage_account_container_name = os.environ.get("SA_CONTAINER_NAME")
poster_folder = os.environ.get("POSTER_LOCATION")