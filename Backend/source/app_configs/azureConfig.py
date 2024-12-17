from azure.storage.blob import BlobServiceClient
import os



def get_az_service_blob_client():
    azure_storage_acc_connection_str = os.getenv("AZURE_STORAGE_ACCOUNT_CONNECTION_STRING")
    container = os.getenv("CONTAINER")

    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_acc_connection_str)
    blob_client = blob_service_client.get_container_client(container)

    return blob_service_client, blob_client