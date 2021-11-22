import json
import os

from saleapp import app
from saleapp.models import Category, Product


# Read Json file
def read_json(path):
    with open(path, "r") as file:
        return json.load(file)

# load data
def load_data(dataPath): 
    return read_json(os.path.join(app.root_path, dataPath))

# Transform python object back into json
# output_json = json.dumps(output_products)

# load products
def load_products(name=''): 
    return Product.query.filter(Product.name.contains(name)).all()

# load categories
def load_categories(name=''): 
    return Category.query.filter(Category.name.contains(name)).all()

# load products by price
def load_products_by_categoryId(categoryId): 
    return Product.query.filter(Product.category_id == categoryId).all()

# load products by price
def load_products_by_price(from_price, to_price): 
    return Product.query.filter(
        Product.price.__gt__(from_price),
        Product.price.__lt__(to_price),
    ).all()
