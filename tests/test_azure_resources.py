try:
    resource_group = resource_client.resource_groups.create_or_update(resource_group_name, resource_group_params)
    print(f"Provisioned Resource Group {resource_group.name} in the {resource_group.location} region.")
except Exception as e:
    print(f"Failed to create Resource Group: {e}")

try:
    container.upsert_item(movie_data)
    print(f"Inserted movie data for '{movie_data['title']}' into the Cosmos DB.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
