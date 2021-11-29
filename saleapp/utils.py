import hashlib

from saleapp import app, db
from saleapp.models import Category, Product, User


# load products
def load_products(category_id=None, name=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if category_id:
        products = products.filter(Product.category_id.__eq__(category_id))
    
    if name:
        products = products.filter(Product.name.__eq__(name))
    
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    
    if to_price:
        products = products.filter(Product.price.__le__(to_price))
    
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()


def count_products():
    return Product.query.count()


def load_categories():
    return Category.query.all()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(
            User.username.__eq__(username),
            User.password.__eq__(password)
        ).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def addUser(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(
        name=name, 
        username=username, 
        password=password, 
        email=kwargs.get('email'), 
        avatar=kwargs.get('avatar'))
    
    db.session.add(user)
    db.session.commit()
