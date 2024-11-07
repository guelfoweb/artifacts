import json
from . import json_file
from prettytable import PrettyTable

def jaccard_similarity(set1, set2):
    # Calculate the Jaccard similarity between two sets
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return 0 if union == 0 else intersection / union

def dataset(lista):
    # Return a set of data extracted from file extensions
    return {p.split('.')[-1] for p in lista}

def get(set_a, all_families, patterns):
    # Get Jaccard similarity statistics for the given patterns and sets
    p = dataset(set_a["permission"])
    a = dataset(set_a["application"])
    i = dataset(set_a["intent"])

    stats = {}
    values = {}

    for _, row in patterns.iterrows():
        # Extract data for comparison
        p1 = dataset(row["permission"])
        a1 = dataset(row["application"])
        i1 = dataset(row["intent"])

        family = row["name"]

        # Calculate Jaccard similarities
        permission = jaccard_similarity(p, p1) * 100
        application = jaccard_similarity(a, a1) * 100
        intent = jaccard_similarity(i, i1) * 100

        # Store calculated values
        values[family] = {
            "permission": round(permission, 2),
            "application": round(application, 2),
            "intent": round(intent, 2)
        }

        # Calculate overall similarity score
        similarity = round((permission + application + intent) / 3, 2)
        stats[family] = similarity

    # Sort families by similarity score in descending order
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    if all_families:
        # Display all families with their statistics in a table
        headers = ['family', 'permission', 'application', 'intent', 'total']
        table = PrettyTable(headers)
        for family, total in sorted_stats:
            permission = values[family]['permission']
            application = values[family]['application']
            intent = values[family]['intent']
            table.add_row([family, permission, application, intent, total])
        return table

    # Return the family with the best match
    best_family = sorted_stats[0][0]
    match = {
        "name": best_family,
        "match": sorted_stats[0][1],
        "value": values[best_family]
    }
    
    return match
