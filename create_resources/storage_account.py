# Import the main module
from azure.storage.blob import BlobServiceClient
import main

# Obtain a client for managing Azure Storage accounts
# StorageManagementClient lets you manage Azure Storage accounts (Blob, File, Table, Queue).
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
# Like CosmosDB, creating a storage account is an asynchronous operation, so we wait for completion with .result().
storage_account = storage_client.storage_accounts.begin_create(main.resource_group_name, main.storage_account_name, storage_account_params).result()
print(f"Provisioned Storage Account {main.storage_account_name} in the Resource Group {main.resource_group_name} in the {storage_account.location} region.")

# Build the blob service client using the storage account
storage_account_url = f"https://{main.storage_account_name}.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=main.credential)

# Create a container in the Blob Storage account
blob_container_client = blob_service_client.create_container(main.storage_account_container_name, public_access='Blob')
print(f"Created Blob container: {main.storage_account_container_name}")