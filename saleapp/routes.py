from flask.templating import render_template
from flask import request
from saleapp import app, utils

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
    _id = int(request.args.get('category_id', 0))

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
    keyword = request.args.get('keyword', 'nokeyword').lower()
    from_price = int(request.args.get('from_price', 0))
    to_price = int(request.args.get('to_price', 0))
    isNameSearch = True if (keyword != 'nokeyword') else False

    # Compare function
    def rangeCompare(product_price):
        return ((product_price >= from_price) and (product_price <= to_price))

    # Transform json input to python objects
    input_products = utils.load_data("data/products.json")

    # Filter by name or by price
    if (isNameSearch):
        output_products = [
            product for product in input_products if product["name"].lower().find(keyword) >= 0
        ]
    else:
         output_products = [
            product for product in input_products if rangeCompare(product["price"])
        ]

    return render_template(
        "./pages/search.html",
        title=('%s Giá tốt nhất' % keyword) if isNameSearch else ('%s VNĐ đến %s VNĐ' % (from_price, to_price)),
        products=input_products,
        filtered_products=output_products,
    )
