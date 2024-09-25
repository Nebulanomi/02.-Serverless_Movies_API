# Import the needed credential and management objects from the libraries
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.storage import StorageManagementClient

###

# Step 1: Acquire credentials
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

###

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

###

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