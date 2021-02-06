from flask import render_template,redirect,flash,url_for,request,Response,current_app,make_response
from blog import app,db,photos
import secrets,os
from blog.forms import RegistrationForm,LoginForm,BrandForm,CategoryForm,AddProductForm,BuyForm
from blog.models import User,Brand,Category,AddProduct,Buy
from flask_login import login_user,logout_user,current_user,login_required
import pdfkit as p


path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = p.configuration(wkhtmltopdf=path_wkhtmltopdf)


@app.route('/')
def index():
    products=AddProduct.query.order_by(AddProduct.date.desc())
    brands=Brand.query.join(AddProduct,(Brand.id==AddProduct.brand_id)).all()
    categories=Category.query.join(AddProduct,(Category.id==AddProduct.category_id)).all()
    return render_template('index.html',products=products,brands=brands,categories=categories)


@app.route('/brand/<int:id>')
def get_brand(id):
    brand=AddProduct.query.filter_by(brand_id=id)
    brands=Brand.query.join(AddProduct,(Brand.id==AddProduct.brand_id)).all()
    categories=Category.query.join(AddProduct,(Category.id==AddProduct.category_id)).all()
    return render_template('index.html',brand=brand,brands=brands,categories=categories)

@app.route('/category/<int:id>')
def get_category(id):
    category=AddProduct.query.filter_by(category_id=id)
    categories=Category.query.join(AddProduct,(Category.id==AddProduct.category_id)).all()
    brands=Brand.query.join(AddProduct,(Brand.id==AddProduct.brand_id)).all()
    return render_template('index.html',category=category,categories=categories,brands=brands)



@app.route('/product/<int:id>')
def single_page(id):
    product=AddProduct.query.get_or_404(id)
    return render_template('single_page.html',product=product)

@app.route('/products')
@login_required
def products():
    products=AddProduct.query.all()
    return render_template('products.html',products=products)
     

@app.route('/get_pdf')
@login_required
def get_pdf():
    products=AddProduct.query.all()
    rendered=render_template('pdf.html',products=products)
    pdf=p.from_string(rendered,False,configuration=config)
    response=make_response(pdf)
    response.headers['content-Type']='application/pdf'
    response.headers['content-Disposition']='inline: filename=output.pdf'
    return response



@app.route('/brands')
@login_required
def brands():
    brands=Brand.query.all()
    return render_template('brands.html',brands=brands)

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
@login_required
def updatebrand(id):
    form=BrandForm()
    updatebrand=Brand.query.get_or_404(id)
    brand=request.form.get('name')
    if request.method=='POST':
        updatebrand.name=brand
        flash(f'Brand Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    elif request.method=='GET':
        form.name.data=updatebrand.name
    return render_template('updatebrand.html',form=form)



@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
@login_required
def updatecategory(id):
    form=CategoryForm()
    updatecategory=Category.query.get_or_404(id)
    category=request.form.get('name')
    if request.method=='POST':
        updatecategory.name=category
        flash(f'Category Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('cotegory'))
    elif request.method=='GET':
        form.name.data=updatecategory.name
    return render_template('updatecategory.html',form=form)








@app.route('/deletebrand/<int:id>',methods=['GET','POST'])
@login_required
def deletebrand(id):
    deletebrand=Brand.query.get_or_404(id)
    db.session.delete(deletebrand)
    db.session.commit()
    flash('Brand Successfully Deleted','success')
    return redirect(url_for('brands'))
    

@app.route('/deletecategory/<int:id>',methods=['GET','POST'])
@login_required
def deletecategory(id):
    deletecategory=Category.query.get_or_404(id)
    db.session.delete(deletecategory)
    db.session.commit()
    flash('Category Successfully Deleted','success')
    return redirect(url_for('index'))


    

@app.route('/categories')
@login_required
def cateogris():
    categories=Category.query.all()
    return render_template('categories.html',categories=categories)

@app.route('/register',methods=['GET','POST'])

def register():

    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data,password=form.password.data).first()
        if user:
            login_user(user)
            flash(f'Welcome You Successfully loged in','success')
            return redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessfull Try again','danger')
    return render_template('login.html',form=form,title='Login')


@app.route('/brand',methods=['GET','POST'])
@login_required
def brand():
    form=BrandForm()
    if form.validate_on_submit():
        brand=Brand(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f'Your Brand Created Succefully','success')
        return redirect(url_for('brands'))
    return render_template('brand.html',title='New Post',form=form)

@app.route('/category',methods=['GET','POST'])
@login_required
def category():
    form=CategoryForm()
    if form.validate_on_submit():
        category=Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Your Category Created Succefully','success')
        return redirect(url_for('category'))

    return render_template('category.html',title='New Post',form=form)

@app.route('/addproduct',methods=['GET','POST'])
@login_required
def addproduct():
    brands=Brand.query.all()
    categories=Category.query.all()
    form=AddProductForm()
    if form.validate_on_submit():
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        desc=form.desc.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        colors=form.colors.data
        image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+".")
        image2=photos.save(request.files.get('image2'),name=secrets.token_hex(10)+".")
        image3=photos.save(request.files.get('image3'),name=secrets.token_hex(10)+".")
        add=AddProduct(name=name,price=price,discount=discount,stock=stock,desc=desc,brand_id=brand,category_id=category,colors=colors,image1=image1,image2=image2,image3=image3)
        db.session.add(add)
        db.session.commit()
        flash(f'Product Created Successfully','success')
        return redirect(url_for('index'))
    return render_template('addproduct.html',form=form,categories=categories,brands=brands)




@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
@login_required
def updateproduct(id):
    brands=Brand.query.all()
    categories=Category.query.all()
    product=AddProduct.query.get_or_404(id)
    form=AddProductForm()
    if form.validate_on_submit():
        product.name=form.name.data
        product.price=form.price.data
        product.discount=form.discount.data
        product.stock=form.stock.data
        product.desc=form.desc.data
        product.colors=form.colors.data
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/img/'+product.image1))
                product.image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+'.')
        
            except:
                product.image1=photos.save(request.files.get('image1'),name=secrets.token_hex(10)+'.')
        if request.files.get('image2'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/img/'+product.image2))
                product.image2=photos.save(request.files.get('image2'),name=secrets.token_hex(10)+'.')
        
            except:
                product.image2=photos.save(request.files.get('image2'),name=secrets.token_hex(10)+'.')
        
        if request.files.get('image3'):
            try:
                os.unlink(os.path.join(current_app.root_path,'static/img/'+product.image3))
                product.image3=photos.save(request.files.get('image3'),name=secrets.token_hex(10)+'.')
            except:
                product.image3=photos.save(request.files.get('image3'),name=secrets.token_hex(10)+".")

                
        flash(f'Product Successfully Updated','success')
        db.session.commit()
        return redirect(url_for('products',product_id=product.id))
    elif request.method=='GET':
        form.name.data=product.name
        form.price.data=product.price
        form.discount.data=product.discount
        form.stock.data=product.stock
        form.desc.data=product.desc
        form.colors.data=product.colors
    return render_template('updateproduct.html',form=form ,brands=brands,categories=categories)




@app.route('/deleteproduct/<int:id>',methods=['GET','POST'])
@login_required
def deleteproduct(id):
    product=AddProduct.query.get_or_404(id)
    os.remove(os.path.join(current_app.root_path,'static/img/'+product.image1))
    os.remove(os.path.join(current_app.root_path,'static/img/'+product.image2))
    os.remove(os.path.join(current_app.root_path,'static/img/'+product.image3))
    db.session.delete(product)
    db.session.commit()
    flash('Product Successfully Deleted','success')
    return redirect(url_for('products'))

@app.route('/buy/<int:id>',methods=['GET','POST'])
@login_required
def buy(id):
    product=AddProduct.query.get_or_404(id)
    form=BuyForm()
    if form.validate_on_submit():  
        buy=Buy(username=form.username.data,add=form.add.data,phnum=form.phnum.data,clnum=form.clnum.data,price =product.price)
        db.session.add(buy)
        db.session.commit()
        flash(f'منتظر ما باشید به زود ترین فرصت با شما تماس میگیریم','success')
        return redirect(url_for('index'))
    return render_template('buy.html',form=form)



@app.route('/buys',methods=['GET','POST'])
@login_required
def buys():
    buys=Buy.query.all()
    x=0
    for buy in buys:
        x+=buy.price*buy.clnum
    return render_template('buys.html',buys=buys,x=x)

@app.route('/deletebuys/<int:id>',methods=['GET','POST'])
@login_required
def deletebuys(id):
    buys=Buy.query.get_or_404(id)
    db.session.delete(buys)
    db.session.commit()
    flash('Buy Successfully Deleted','success')
    return redirect(url_for('buys'))


@app.route('/get_pdf_buy')
@login_required
def get_pdf_buy():
    buys=Buy.query.all()
    x=0
    for buy in buys:
        x+=buy.price*buy.clnum
    rendered=render_template('pdfbuy.html',buys=buys,x=x)
    pdf=p.from_string(rendered,False,configuration=config)
    response=make_response(pdf)
    response.headers['content-Type']='application/pdf'
    response.headers['content-Disposition']='inline: filename=outputbuy.pdf'
    return response

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

