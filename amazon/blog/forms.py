from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from blog.models import User,Brand,Category
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=100)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The Username Exist')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The Email Exist')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')


class BrandForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    submit=SubmitField('Post')
    def validate_name(self, name):
        if name.data != self.name:
            brand = Brand.query.filter_by(name=self.name.data).first()
            if brand is not None:
                raise ValidationError('Please use a different name.')

class CategoryForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    submit=SubmitField('Post')
    def validate_name(self, name):
        if name.data != self.name:
            category = Category.query.filter_by(name=self.name.data).first()
            if category is not None:
                raise ValidationError('Please use a different name.')

class AddProductForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    discount=IntegerField('Discount',default=0)
    stock=IntegerField('Stock',validators=[DataRequired()])
    desc=TextAreaField('Description',validators=[DataRequired()])
    colors=TextAreaField('Colors',validators=[DataRequired()])
    image1=FileField('Image 1',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    image2=FileField('Image 2',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    image3=FileField('Image 3',validators=[FileRequired(),FileAllowed(['jpg','png','gif','jpeg'])])
    submit=SubmitField('Submit')

class BuyForm(FlaskForm):
    username=StringField('نام شما',validators=[DataRequired()])
    add=StringField('آدرس فعلی شما',validators=[DataRequired()])
    phnum=IntegerField('نمبر تلیفون شما',validators=[DataRequired()])
    clnum=IntegerField('از این کالا چند دانه میخواهین',validators=[DataRequired()])
    submit=SubmitField('تایید')