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