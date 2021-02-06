from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
from flask_admin import Admin
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
import os
from flask_security import Security,SQLAlchemyUserDatastore,UserMixin,RoleMixin



basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY']='7cadfb11d2432da5a235e8f6327e310173260b029200db1993fc36b738f8d677'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/img')





photos=UploadSet('photos',IMAGES)
configure_uploads(app,photos)
patch_request_class(app)


db=SQLAlchemy(app)
login_manager=LoginManager(app)
from blog import routes