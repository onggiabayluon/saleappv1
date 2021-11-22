from flask.templating import render_template
from flask import request
from saleapp import app, utils
# Import admin 
from saleapp.admin import *


@app.route('/')
def home():
    print(utils.load_products())
    # Load all Products
    return render_template(
        "./pages/home.html",
        title="Tất cả sản phẩm",
        products=utils.load_products(),
        categories=utils.load_categories()
    )


# products Route
@app.route('/products', methods=['GET'])
def products():
    # get parameters
    _id = int(request.args.get('category_id', 0))

    # Filter python objects with list comprehensions
    output_products = utils.load_products_by_categoryId(_id)

    return render_template(
        "./pages/products.html",
        title="Products",
        products=output_products,
    )

# search Route
@app.route('/search', methods=['GET'])
def search():
    # get parameters
    keyword = request.args.get('keyword', 'undefined').lower()
    from_price = int(request.args.get('from_price', 0))
    to_price = int(request.args.get('to_price', 0))
    searchByName = True if (keyword != 'undefined') else False 

    # Filter by name or by price
    if (searchByName):
        output_products = utils.load_products(keyword)
    else:
        output_products = utils.load_products_by_price(from_price, to_price)

    return render_template(
        "./pages/search.html",
        title=('%s Giá tốt nhất' % keyword) if searchByName else ('%s VNĐ đến %s VNĐ' % (from_price, to_price)),
        products=utils.load_products(),
        filtered_products=output_products,
    )
