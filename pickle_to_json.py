import pickle
import json

# Step 1: Load data from pickle file
a = "list_hierarchy_expected"
pickle_file = f'{a}.pickle'
json_file = f'{a}.json'

with open(pickle_file, 'rb') as f:
    data = pickle.load(f)

# Step 2: Convert Python objects to JSON-serializable format
# Assuming 'data' is a Python object you want to serialize to JSON
# Here, we'll convert it to a dictionary
json_data = {}

if isinstance(data, dict):
    json_data = data
elif isinstance(data, list):
    json_data['list_data'] = data
else:
    # Handle other types as needed
    pass

# Step 3: Serialize to JSON
json_string = json.dumps(json_data, indent=4)

# Step 4: Write JSON to file
with open(json_file, 'w') as f:
    f.write(json_string)

print(f'Converted {pickle_file} to {json_file}')
