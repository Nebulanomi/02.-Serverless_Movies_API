# Import the main module
import main

# Obtain a client for managing Azure Resource Groups
# ResourceManagementClient allows us to interact with Azure Resource Groups.
resource_client = main.ResourceManagementClient(main.credential, main.subscription_id)

resource_group_params = {
    "location": main.location,
    "tags": {
        "Budget": "0€",
        "End date": "Never",
        "Owner" : "Alexandre Pereira",
        "Secondary Owner" : "None",
        "Team name" : "None"
    }
}

# Create the Resource Group
# This API call creates or updates a resource group in the specified region.
resource_group = resource_client.resource_groups.create_or_update(main.resource_group_name, resource_group_params)
print(f"Provisioned Resource Group {resource_group.name} in the {resource_group.location} region.")