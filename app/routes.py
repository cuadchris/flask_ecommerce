from crypt import methods
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import User, CartItem
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.products import *

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    products = get5RandomProducts()
    for i in products:
        print(i['image'])
    return render_template('index.html', title = 'Home', products=products, itemsInCart=itemsInCart)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# 'GET' request will return template, 'POST' request will add to shopping cart.
@app.route('/product/<item>', methods = ['GET', 'POST'])
def product(item):
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    item = getProduct(item)
    if request.method == 'POST':
        current_item = CartItem.query.filter_by(product_id=item['id']).first()
        if current_item:
            new_total = int(current_item.quantity) + int(request.form['quantity'])
            current_item.quantity = new_total
            db.session.commit()
            flash("You had these in your cart already, so we've updated the quantity.")
            return redirect(url_for('product', item=current_item.product_id))
        else:
            product = CartItem()
            product.user_id = current_user.id
            product.product_id = item['id']
            product.quantity = request.form['quantity']
            db.session.add(product)
            db.session.commit()
            flash('Item added to cart!')
            return redirect(url_for('product', item=product.product_id))
    return render_template('product.html', title='Product', item=item, itemsInCart=itemsInCart)

# @app.route('/category')
# def category():
#     products = get5RandomProducts()
#     return render_template('category.html', products=products)

@app.route('/smartphones')
def smartPhones():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    data = getCategory('smartphones')
    return render_template('categories.html', title='Smartphones', data=data, itemsInCart=itemsInCart)

@app.route('/mensshoes')
def mensShoes():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    data = getCategory('mens-shoes')
    return render_template('categories.html', title="Men's Shoes", data=data, itemsInCart=itemsInCart)

@app.route('/womensshoes')
def womensShoes():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    data = getCategory('womens-shoes')
    return render_template('categories.html', title="Women's Shoes", data=data, itemsInCart=itemsInCart)

@app.route('/cart')
@login_required
def cart():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    cartinfo = CartItem.query.filter_by(user_id = current_user.id).all()
    cart = []
    for item in cartinfo:
        cart.append(getProduct(item.product_id))
    quantities = [x.quantity for x in cartinfo]
    prices = [x['price'] for x in cart]
    joined = zip(quantities, prices)
    total = sum(x*y for x,y in joined)

    return render_template('cart.html', title='Cart', cart=cart, cartinfo=cartinfo, total=total, itemsInCart=itemsInCart)

@app.route('/editcart', methods = ['GET', 'POST'])
@login_required
def editCart():
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        if not items:
            itemsInCart = ''
        else:
            itemsInCart = len(items)
    else:
        itemsInCart = ''
    cartinfo = CartItem.query.filter_by(user_id = current_user.id).all()
    cart = []
    for item in cartinfo:
        cart.append(getProduct(item.product_id))
    return render_template('editcart.html', title="Edit Cart", cartinfo=cartinfo, cart=cart, itemsInCart=itemsInCart )

@app.post('/updateitem')
@login_required
def updateItem():
    data = request.get_json() # {'product_id': '59', 'quantity': '10'}
    item = CartItem.query.filter_by(product_id=data['product_id']).first()
    item.quantity = data['quantity']
    db.session.commit()
    return {'response': 'ok'}

@app.post('/removeitem')
@login_required
def removeItem():
    data = request.get_json()
    item = CartItem.query.filter_by(product_id=data).first()
    db.session.delete(item)
    db.session.commit()
    return {'response': 'ok'}

@app.route('/emptycart')
@login_required
def emptyCart():
    items = CartItem.query.all()
    for i in items:
        db.session.delete(i)
    db.session.commit()
    return {'response': 'ok'}