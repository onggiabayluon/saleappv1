import math

import cloudinary.uploader
from flask import request, url_for
from flask.templating import render_template
from flask_login import login_user, logout_user
from werkzeug.utils import redirect

from saleapp import app, login_manager, utils
# Import admin 
from saleapp.admin import *


@app.context_processor
def inject_categories():
    return {
        'categories': utils.load_categories()
    }

@login_manager.user_loader    
def inject_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/')
def home():
    # Load all Products
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)
    cate_id = request.args.get('category_id')
    products = utils.load_products(category_id=cate_id, name=kw, page=int(page))
    products_size = utils.count_products()
    
    return render_template(
        "./pages/home.html",
        title="Tất cả sản phẩm",
        products=products,
        pages=math.ceil(products_size/app.config['PAGE_SIZE']))


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
        output_products = utils.load_products(name=keyword)
    else:
        output_products = utils.load_products(from_price=from_price, to_price=to_price)

    return render_template(
        "./pages/search.html",
        title=('%s Giá tốt nhất' % keyword) if searchByName else ('%s VNĐ đến %s VNĐ' % (from_price, to_price)),
        products=utils.load_products(),
        filtered_products=output_products,
    )


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    err_msg = ""
    if request.method == 'POST':
        # lay du lieu trong request form
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        avatar = request.files['avatar']
        avatar_path = None

        # them vao db
        try:
            if password == confirm:
                if avatar:
                    upload_result = cloudinary.uploader.upload(avatar)
                    avatar_path = upload_result['secure_url']

                utils.addUser(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = "Wrong password"
        except Exception as exception:
            err_msg = 'Error from server: ' + str(exception)

    return render_template(
        "./pages/register.html",
        title="Register New User",
        err_msg=err_msg
    )

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = utils.check_login(username=username, password=password)
        
        if user:
            login_user(user)
            print("logib status:%s" % login_user(user))
            print(user.name) # output a name
            return redirect(url_for('home'))
        else:
            err_msg = "Wrong username or password"

    return render_template(
        "./pages/login.html",
        title="Login",
        err_msg=err_msg
    )

@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))
