import hashlib

from flask_login import current_user
from sqlalchemy.sql.functions import func

from saleapp import app, db
from saleapp.models import (Category, Product, Receipt, ReceiptDetail, User,
                            UserRole)


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


def check_login(username, password, role=UserRole.USER):
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

def cate_stats():
    return Category.query.join(Product,
                               Product.category_id.__eq__(Category.id),
                               isouter=True)\
                    .add_columns(func.count(Product.id))\
                    .group_by(Category.id).all()

def cate_stats2():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id, Category.name).all()


def get_cart_checkout(carts):
    total_quantity, total_amount = 0, 0

    if carts:
        for cart in carts.values():
            total_quantity += cart['quantity']
            total_amount += cart['quantity'] * cart['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

def add_receipt(carts):
    if carts:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)
        
        for cart in carts.values():
            receipt_detail = ReceiptDetail(receipt=receipt,
                              product_id=cart['id'],
                              quantity=cart['quantity'],
                              unit_price=cart['price'])
            db.session.add(receipt_detail)

        db.session.commit()
