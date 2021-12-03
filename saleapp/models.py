from datetime import datetime
from enum import Enum as UserEnum

from flask_login import UserMixin
from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Enum
from sqlalchemy.types import TypeDecorator

from saleapp import db

# custom augmented string type: Strip String
# class String(TypeDecorator):
#     impl = db.String

#     def process_bind_param(self, value, dialect):
#         # In case you have nullable String fields and pass None
#         return value.strip() if value else value

#     def copy(self, **kw):
#         return String(self.impl.length)


class BaseModel(db.Model):
    # Bảng trung gian cho các bảng khác, và không muốn tạo bảng này khi db.create_all()
    # thì ta phải dùng lệnh __abstract__
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = "category"

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)
    def __str__(self):
        return self.name

# Bảng trung gian
product_tag = db.Table('product_tag', 
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True), # Khóa chính
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True) # Khóa chính
)


class Product(BaseModel):
    __tablename__ = "product"

    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    # lazy=subquery: Truy cập 1 product tự động truy vấn danh sach tags luôn
    # backref (lazy=true): Bấm tag nào thì mới query product của tag đó
    # chứ không truy vấn tag và product cùng 1 lúc khi 
    tags = relationship('Tag', secondary='product_tag', lazy='subquery', 
                        backref=backref('products', lazy=True)) 
    def __str__(self):
            return self.name

class Tag(BaseModel):
    __tablename__ = "tag"
    name = Column(String(50), nullable=False, unique=True)
    def __str__(self):
        return self.name


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)
    

class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)

if __name__ == '__main__':
    db.create_all()
    # c1 = Category(name="Mobile")
    # c2 = Category(name="tablet")

    # p1 = Product(name='Mobile',description='Apple, 32GB, RAM: 3GB, iOS13',price="17000000",image='https://cdn.tgdd.vn/Products/Images/42/78124/iphone-7-plus-gold-400x460-400x460.png',category_id=1)
    # p2 = Product(name='iPad Pro 2020',description='Apple, 128GB, RAM: 6GB',price="37000000",image='https://cdn.tgdd.vn/Products/Images/522/221775/ipad-pro-12-9-inch-wifi-128gb-2020-xam-400x460-1-400x460.png', category_id= 2)
    
    # t1 = Tag(name='new')
    # t2 = Tag(name='promotion')

    # db.session.add(c1)
    # db.session.add(c2)

    # db.session.add(p1)
    # db.session.add(p2)

    # db.session.add(t1)
    # db.session.add(t2)

    # db.session.commit()
