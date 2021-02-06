from blog import db,app
from blog import login_manager
from flask_login import UserMixin,current_user
from datetime import datetime
from wtforms.validators import ValidationError
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)

class AddProduct(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    discount=db.Column(db.Integer,default=0)
    stock=db.Column(db.Integer,nullable=False)
    desc=db.Column(db.Text,nullable=False)
    
    brand_id=db.Column(db.Integer,db.ForeignKey('brand.id'))
    brand=db.relationship('Brand',backref=db.backref('brands',lazy=True))
    
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
    category=db.relationship('Category',backref=db.backref('categories',lazy=True))

    buy_id=db.Column(db.Integer,db.ForeignKey('buy.id'))
    buy=db.relationship('Buy',backref=db.backref('buys',lazy=True))

    colors=db.Column(db.String(80),nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    image1=db.Column(db.String(150),nullable=False,default='image.jpg')
    image2=db.Column(db.String(150),nullable=False,default='image.jpg')
    image3=db.Column(db.String(150),nullable=False,default='image.jpg')
    
    def __repr__(self):
        return f"AddProduct('{self.name}','{self.price}')"
class Brand(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    name=db.Column(db.String(20),nullable=False)
   
    def __repr__(self):
        return f"Brand('{self.name}')"



class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    name=db.Column(db.String(20),nullable=False)
    def __repr__(self):
        return f"Category('{self.name}')"

class Buy(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    username=db.Column(db.Integer,nullable=False)
    add=db.Column(db.String(100),nullable=False)
    phnum=db.Column(db.Integer,nullable=False)
    clnum=db.Column(db.Integer,nullable=False)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    price=db.Column(db.Integer,nullable=False)



