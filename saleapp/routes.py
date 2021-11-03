from flask.templating import render_template
from flask import request
from saleapp import app, utils
import sys, json

@app.route('/')
def home():
    # Load all Products
    products = utils.load_data("data/products.json")
    return render_template(
        "./pages/home.html",
        title="Tất cả sản phẩm",
        products=products,
        categories=utils.load_data("data/categories.json")
    )


# products Route
@app.route('/products', methods=['GET'])
def products():
    # get parameters
    _id = int(request.args.get('category_id')) if request.args.get('category_id') else None

    # Transform json input to python objects
    input_products = utils.load_data("data/products.json")

    # Filter python objects with list comprehensions
    output_products = [product for product in input_products if product["category_id"] == _id ]

    return render_template(
        "./pages/products.html",
        title="Products",
        products=output_products,
    )

# search Route
@app.route('/search', methods=['GET'])
def search():
    # get parameters
    keyword = request.args.get('keyword').lower()

    # Transform json input to python objects
    input_products = utils.load_data("data/products.json")

    # Filter python objects with list comprehensions
    output_products = [
        product for product in input_products if product["name"].lower().find(keyword) >= 0 
    ]

    return render_template(
        "./pages/products.html",
        title='%s Giá tốt nhất' % keyword,
        products=output_products,
    )
