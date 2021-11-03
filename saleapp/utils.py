import json
import os

from saleapp import app


# Read Json file
def read_json(path):
    with open(path, "r") as file:
        return json.load(file)

# load data
def load_data(dataPath): 
    return read_json(os.path.join(app.root_path, dataPath))

# Transform python object back into json
# output_json = json.dumps(output_products)
