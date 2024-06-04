# paperbackcollections/views.py
from flask import render_template, redirect, url_for, request, flash
from . import db
from .models import Product, Order
from .forms import CheckoutForm
from flask import current_app as app

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart():
    orders = Order.query.all()
    return render_template('cart.html', orders=orders)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        order = Order(
            customer_name=form.name.data,
            customer_address=form.address.data,
            customer_email=form.email.data,
            # Add more logic here to associate products with the order
        )
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('checkout.html', form=form)
