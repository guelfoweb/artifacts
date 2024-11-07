import os
from . import json_file

def get(activity):
    # Load permission categories and descriptions
    permission_categories = json_file.load_json("permission_categories.json")
    permission_description = json_file.load_json("permission_description.json")

    categories = {}
    not_category = []

    # Check if "permission" is in the activity
    permissions = activity.get("permission")
    if not permissions:
        print("Permission not found")
        return categories

    # Process the permission list
    permission_list = [item.split('.')[-1] for item in permissions]

    # Categorize the permissions
    for perm in permission_list:
        # Try to find the permission in the categories
        matched = False
        for category, perm_list in permission_categories.items():
            if perm in perm_list:
                # Get the description for the permission if available
                desc = permission_description.get(perm, "")
                
                # Add the permission to the respective category
                categories.setdefault(category, []).append((perm, desc))
                matched = True
                break
        
        # If permission doesn't match any category, add to not_category list
        if not matched:
            not_category.append(perm)

    return categories
