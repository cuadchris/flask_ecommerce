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
    products = get5RandomProducts()
    for i in products:
        print(i['image'])
    return render_template('index.html', title = 'Home', products=products)


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
    item = getProduct(item)
    if request.method == 'POST':
        product = CartItem()
        product.user_id = current_user.id
        product.product_id = item['id']
        product.quantity = request.form['quantity']
        db.session.add(product)
        db.session.commit()
    return render_template('product.html', title='Product', item=item)