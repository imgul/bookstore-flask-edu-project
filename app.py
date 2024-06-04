from flask import flash, Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a very secret key'  # Change this to a real secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    published_on = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    reviews = db.Column(db.Integer, nullable=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='carts')

# Forms
class AddToBasketForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Basket')


class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/static/<path:filename>')
def send_static_file(filename):
    return send_file(f'static/{filename}', cache_timeout=0)  # Set cache timeout to 0

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToBasketForm()
    return render_template('product_detail.html', product=product, form=form)

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    # quantity = int(request.form['quantity'])
    quantity = 1
    cart = Cart(product_id=product_id, quantity=quantity)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('basket'))

# remove cart item
@app.route('/remove-from-cart/<int:cart_id>')
def remove_from_cart(cart_id):
    cart = Cart.query.get_or_404(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('basket'))

@app.route('/basket', methods=['GET', 'POST'])
def basket():
    carts = Cart.query.all()
    return render_template('basket.html', carts=carts)

# @app.route('/checkout', methods=['GET', 'POST'])
# def checkout():
#     form = CheckoutForm()
#     carts = Cart.query.all()
#     if form.validate_on_submit():
#         Cart.query.delete()
#         db.session.commit()
#         return render_template('checkout.html', orders=[], checkout_success=True, form=form)
#     return render_template('checkout.html', carts=carts, form=form)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    carts = Cart.query.all()
    if form.validate_on_submit():
        # Process the form data (e.g., create an order, clear the cart)
        Cart.query.delete()
        db.session.commit()
        flash('Checkout successful!', 'success')
        return redirect(url_for('checkout_success'))
    return render_template('checkout.html', carts=carts, form=form)

@app.route('/checkout_success')
def checkout_success():
    return render_template('checkout_success.html')

fiction_books = [
    Product(
        title='You Like It Darker: Stories',
        author='Stephen King',
        price=18.90,
        description='''From legendary storyteller and master of short fiction Stephen King comes an extraordinary new collection of twelve short stories, many never-before-published, and some of his best EVER.

                “You like it darker? Fine, so do I,” writes Stephen King in the afterword to this magnificent new collection of twelve stories that delve into the darker part of life—both metaphorical and literal. King has, for half a century, been a master of the form, and these stories, about fate, mortality, luck, and the folds in reality where anything can happen, are as rich and riveting as his novels, both weighty in theme and a huge pleasure to read. King writes to feel “the exhilaration of leaving ordinary day-to-day life behind,” and in You Like It Darker, readers will feel that exhilaration too, again and again.

                “Two Talented Bastids” explores the long-hidden secret of how the eponymous gentlemen got their skills. In “Danny Coughlin’s Bad Dream,” a brief and unprecedented psychic flash upends dozens of lives, Danny’s most catastrophically. In “Rattlesnakes,” a sequel to Cujo, a grieving widower travels to Florida for respite and instead receives an unexpected inheritance—with major strings attached. In “The Dreamers,” a taciturn Vietnam vet answers a job ad and learns that there are some corners of the universe best left unexplored. “The Answer Man” asks if prescience is good luck or bad and reminds us that a life marked by unbearable tragedy can still be meaningful.

                King’s ability to surprise, amaze, and bring us both terror and solace remains unsurpassed. Each of these stories holds its own thrills, joys, and mysteries; each feels iconic. You like it darker? You got it.''',
        isbn='978-1668037713',
        category='Fiction',
        image='https://m.media-amazon.com/images/I/71UTAmoNddL._SL1500_.jpg',
        publisher='Scribner',
        published_on=datetime.strptime("May 21, 2024", "%B %d, %Y"),
        rating=5.5,
        reviews=500
    ),
    Product(
        title='The Last House Guest',
        author='Megan Miranda',
        price=12.99,
        description='''A Reclusive heiress, a reformed con artist, and a charming new neighbor collide in this riveting tale of secrets, lies, and the search for a truth that may be hiding in plain sight.
        From the New York Times bestselling author of The Last Time I Lied and The Stranger Diaries comes a gripping new novel about a woman who must uncover the secrets of her own past in order to uncover the truth about her new neighbor.

        Ava is a reclusive heiress who has spent her life hiding from the world. She is a master of disguise and deception, but her latest neighbor may be the one person who can see through her facade.

        Lucas is a charming and handsome new neighbor who is hiding secrets of his own. He is a former con artist who has turned his life around, but his past is still shrouded in mystery.

        As Ava and Lucas get to know each other, they must navigate a web of lies and secrets that threaten to destroy their budding relationship. But as they dig deeper into each other's pasts, they may uncover a truth that is hiding in plain sight.

        The Last House Guest is a riveting tale of secrets, lies, and the search for truth that will keep you on the edge of your seat until the very end.''',
        isbn='978-1501144365',
        category='Fiction',
        image='https://m.media-amazon.com/images/I/815oQ6G6HDL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("June 1, 2020", "%B %d, %Y"),
        rating=4.5,
        reviews=250
    ),
    Product(
        title='The Maid',
        author='Nita Prose',
        price=14.99,
        description=''''A charming and riveting psychological thriller about a maid who becomes embroiled in a mystery at a luxurious hotel, from the New York Times bestselling author of The Silent Patient.
        Molly Gray is a maid at the Grand Regency Hotel, where she has worked for over a decade. She is a hard worker and takes great pride in her job, but she is also a bit of a loner.

        One day, Molly discovers the body of a wealthy guest in one of the hotel rooms. The police investigation that follows reveals that the guest was murdered, and Molly becomes the prime suspect.

        As Molly tries to clear her name, she uncovers a web of secrets and lies that threaten to destroy her life. She must navigate a complex cast of characters, including the hotel's wealthy and powerful guests, to uncover the truth about the murder.

        The Maid is a riveting psychological thriller about a woman who will stop at nothing to uncover the truth and clear her name. It is a must-read for fans of The Silent Patient and other psychological thrillers.''',
        isbn='978-1982168971',
        category='Fiction',
        image='https://m.media-amazon.com/images/I/719X2q+QV5L._SL1500_.jpg',
        publisher='Viking',
        published_on=datetime.strptime("January 4, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=200
    ),
    Product(
        title='The Paris Apartment',
        author='Lucy Foley',
        price=16.99,
        description=''''A riveting and atmospheric psychological thriller about a woman who discovers a dark secret in her friend's Paris apartment, from the New York Times bestselling author of The Guest List.
        Jess is a journalist who has just arrived in Paris to visit her friend, Ben. But when she arrives at his apartment, she finds it empty and a mysterious note that suggests Ben has disappeared.

        As Jess searches for Ben, she uncovers a dark secret about his past that threatens to destroy their friendship. She must navigate a complex cast of characters, including Ben's wealthy and powerful friends, to uncover the truth about his disappearance.

        The Paris Apartment is a riveting and atmospheric psychological thriller about a woman who will stop at nothing to uncover the truth about her friend's disappearance. It is a must-read for fans of The Guest List and other psychological thrillers.''',
        isbn='978-0062852583',
        category='Fiction',
        image='https://m.media-amazon.com/images/I/810PcNuumRL._SL1500_.jpg',
        publisher='William Morrow',
        published_on=datetime.strptime("February 22, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=150
    ),
    Product(
        title='The Last Thing He Told Me',
        author='Laura Dave',
        price=14.99,
        description='''A riveting and emotional psychological thriller about a woman who discovers a dark secret about her husband's past, from the New York Times bestselling author of Eight Hundred Grapes.
        Hannah Hall is a successful businesswoman who has it all - a loving husband, a beautiful home, and a fulfilling career. But when her husband disappears without a trace, Hannah's life is turned upside down.

        As she searches for her husband, Hannah uncovers a dark secret about his past that threatens to destroy their marriage. She must navigate a complex cast of characters, including her husband's mysterious colleagues and a detective who is determined to uncover the truth.

        The Last Thing He Told Me is a riveting and emotional psychological thriller about a woman who will stop at nothing to uncover the truth about her husband's disappearance. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1509840244',
        category='Fiction',
        image='https://m.media-amazon.com/images/I/81+TvkWc-uL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("May 4, 2021", "%B %d, %Y"),
        rating=4.5,
        reviews=300
    ),
    Product(
        title='The Silent Patient',
        author='Alex Michaelides',
        price=12.99,
        description='''A psychological thriller about a famous painter who shoots her husband and refuses to speak or cooperate with the police, and the psychotherapist who becomes obsessed with uncovering her secrets.
        Alicia Berenson is a famous painter who has it all - a loving husband, a beautiful home, and a successful career. But when she shoots her husband without warning, her life is turned upside down.

        Theo Faber is a psychotherapist who becomes obsessed with uncovering Alicia's secrets. As he delves deeper into her past, he uncovers a web of secrets and lies that threaten to destroy everything he thought he knew about her.

        The Silent Patient is a psychological thriller about a woman who will stop at nothing to keep her secrets buried. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1250301699',
        category='Fiction',
        image='https://m.media-amazon.com/images/I/71s6siGLrFL._SL1500_.jpg',
        publisher='Celadon Books',
        published_on=datetime.strptime("February 5, 2019", "%B %d, %Y"),
        rating=4.5,
        reviews=400
    ),
    # Add more products here
]

non_fiction_books = [
    Product(
        title='You Like It Darker: Stories',
        author='Stephen King',
        price=18.90,
        description='''From legendary storyteller and master of short fiction Stephen King comes an extraordinary new collection of twelve short stories, many never-before-published, and some of his best EVER.

                “You like it darker? Fine, so do I,” writes Stephen King in the afterword to this magnificent new collection of twelve stories that delve into the darker part of life—both metaphorical and literal. King has, for half a century, been a master of the form, and these stories, about fate, mortality, luck, and the folds in reality where anything can happen, are as rich and riveting as his novels, both weighty in theme and a huge pleasure to read. King writes to feel “the exhilaration of leaving ordinary day-to-day life behind,” and in You Like It Darker, readers will feel that exhilaration too, again and again.

                “Two Talented Bastids” explores the long-hidden secret of how the eponymous gentlemen got their skills. In “Danny Coughlin’s Bad Dream,” a brief and unprecedented psychic flash upends dozens of lives, Danny’s most catastrophically. In “Rattlesnakes,” a sequel to Cujo, a grieving widower travels to Florida for respite and instead receives an unexpected inheritance—with major strings attached. In “The Dreamers,” a taciturn Vietnam vet answers a job ad and learns that there are some corners of the universe best left unexplored. “The Answer Man” asks if prescience is good luck or bad and reminds us that a life marked by unbearable tragedy can still be meaningful.

                King’s ability to surprise, amaze, and bring us both terror and solace remains unsurpassed. Each of these stories holds its own thrills, joys, and mysteries; each feels iconic. You like it darker? You got it.''',
        isbn='978-1668037713',
        category='Non Fiction',
        image='https://m.media-amazon.com/images/I/71UTAmoNddL._SL1500_.jpg',
        publisher='Scribner',
        published_on=datetime.strptime("May 21, 2024", "%B %d, %Y"),
        rating=5.5,
        reviews=500
    ),
    Product(
        title='The Last House Guest',
        author='Megan Miranda',
        price=12.99,
        description='''A Reclusive heiress, a reformed con artist, and a charming new neighbor collide in this riveting tale of secrets, lies, and the search for a truth that may be hiding in plain sight.
        From the New York Times bestselling author of The Last Time I Lied and The Stranger Diaries comes a gripping new novel about a woman who must uncover the secrets of her own past in order to uncover the truth about her new neighbor.

        Ava is a reclusive heiress who has spent her life hiding from the world. She is a master of disguise and deception, but her latest neighbor may be the one person who can see through her facade.

        Lucas is a charming and handsome new neighbor who is hiding secrets of his own. He is a former con artist who has turned his life around, but his past is still shrouded in mystery.

        As Ava and Lucas get to know each other, they must navigate a web of lies and secrets that threaten to destroy their budding relationship. But as they dig deeper into each other's pasts, they may uncover a truth that is hiding in plain sight.

        The Last House Guest is a riveting tale of secrets, lies, and the search for truth that will keep you on the edge of your seat until the very end.''',
        isbn='978-1501144365',
        category='Non Fiction',
        image='https://m.media-amazon.com/images/I/815oQ6G6HDL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("June 1, 2020", "%B %d, %Y"),
        rating=4.5,
        reviews=250
    ),
    Product(
        title='The Maid',
        author='Nita Prose',
        price=14.99,
        description=''''A charming and riveting psychological thriller about a maid who becomes embroiled in a mystery at a luxurious hotel, from the New York Times bestselling author of The Silent Patient.
        Molly Gray is a maid at the Grand Regency Hotel, where she has worked for over a decade. She is a hard worker and takes great pride in her job, but she is also a bit of a loner.

        One day, Molly discovers the body of a wealthy guest in one of the hotel rooms. The police investigation that follows reveals that the guest was murdered, and Molly becomes the prime suspect.

        As Molly tries to clear her name, she uncovers a web of secrets and lies that threaten to destroy her life. She must navigate a complex cast of characters, including the hotel's wealthy and powerful guests, to uncover the truth about the murder.

        The Maid is a riveting psychological thriller about a woman who will stop at nothing to uncover the truth and clear her name. It is a must-read for fans of The Silent Patient and other psychological thrillers.''',
        isbn='978-1982168971',
        category='Non Fiction',
        image='https://m.media-amazon.com/images/I/719X2q+QV5L._SL1500_.jpg',
        publisher='Viking',
        published_on=datetime.strptime("January 4, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=200
    ),
    Product(
        title='The Paris Apartment',
        author='Lucy Foley',
        price=16.99,
        description=''''A riveting and atmospheric psychological thriller about a woman who discovers a dark secret in her friend's Paris apartment, from the New York Times bestselling author of The Guest List.
        Jess is a journalist who has just arrived in Paris to visit her friend, Ben. But when she arrives at his apartment, she finds it empty and a mysterious note that suggests Ben has disappeared.

        As Jess searches for Ben, she uncovers a dark secret about his past that threatens to destroy their friendship. She must navigate a complex cast of characters, including Ben's wealthy and powerful friends, to uncover the truth about his disappearance.

        The Paris Apartment is a riveting and atmospheric psychological thriller about a woman who will stop at nothing to uncover the truth about her friend's disappearance. It is a must-read for fans of The Guest List and other psychological thrillers.''',
        isbn='978-0062852583',
        category='Non Fiction',
        image='https://m.media-amazon.com/images/I/810PcNuumRL._SL1500_.jpg',
        publisher='William Morrow',
        published_on=datetime.strptime("February 22, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=150
    ),
    Product(
        title='The Last Thing He Told Me',
        author='Laura Dave',
        price=14.99,
        description='''A riveting and emotional psychological thriller about a woman who discovers a dark secret about her husband's past, from the New York Times bestselling author of Eight Hundred Grapes.
        Hannah Hall is a successful businesswoman who has it all - a loving husband, a beautiful home, and a fulfilling career. But when her husband disappears without a trace, Hannah's life is turned upside down.

        As she searches for her husband, Hannah uncovers a dark secret about his past that threatens to destroy their marriage. She must navigate a complex cast of characters, including her husband's mysterious colleagues and a detective who is determined to uncover the truth.

        The Last Thing He Told Me is a riveting and emotional psychological thriller about a woman who will stop at nothing to uncover the truth about her husband's disappearance. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1509840244',
        category='Non Fiction',
        image='https://m.media-amazon.com/images/I/81+TvkWc-uL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("May 4, 2021", "%B %d, %Y"),
        rating=4.5,
        reviews=300
    ),
    Product(
        title='The Silent Patient',
        author='Alex Michaelides',
        price=12.99,
        description='''A psychological thriller about a famous painter who shoots her husband and refuses to speak or cooperate with the police, and the psychotherapist who becomes obsessed with uncovering her secrets.
        Alicia Berenson is a famous painter who has it all - a loving husband, a beautiful home, and a successful career. But when she shoots her husband without warning, her life is turned upside down.

        Theo Faber is a psychotherapist who becomes obsessed with uncovering Alicia's secrets. As he delves deeper into her past, he uncovers a web of secrets and lies that threaten to destroy everything he thought he knew about her.

        The Silent Patient is a psychological thriller about a woman who will stop at nothing to keep her secrets buried. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1250301699',
        category='Non Fiction',
        image='https://m.media-amazon.com/images/I/71s6siGLrFL._SL1500_.jpg',
        publisher='Celadon Books',
        published_on=datetime.strptime("February 5, 2019", "%B %d, %Y"),
        rating=4.5,
        reviews=400
    ),
    # Add more products here
]

si_fi_books = [
    Product(
        title='You Like It Darker: Stories',
        author='Stephen King',
        price=18.90,
        description='''From legendary storyteller and master of short fiction Stephen King comes an extraordinary new collection of twelve short stories, many never-before-published, and some of his best EVER.

                “You like it darker? Fine, so do I,” writes Stephen King in the afterword to this magnificent new collection of twelve stories that delve into the darker part of life—both metaphorical and literal. King has, for half a century, been a master of the form, and these stories, about fate, mortality, luck, and the folds in reality where anything can happen, are as rich and riveting as his novels, both weighty in theme and a huge pleasure to read. King writes to feel “the exhilaration of leaving ordinary day-to-day life behind,” and in You Like It Darker, readers will feel that exhilaration too, again and again.

                “Two Talented Bastids” explores the long-hidden secret of how the eponymous gentlemen got their skills. In “Danny Coughlin’s Bad Dream,” a brief and unprecedented psychic flash upends dozens of lives, Danny’s most catastrophically. In “Rattlesnakes,” a sequel to Cujo, a grieving widower travels to Florida for respite and instead receives an unexpected inheritance—with major strings attached. In “The Dreamers,” a taciturn Vietnam vet answers a job ad and learns that there are some corners of the universe best left unexplored. “The Answer Man” asks if prescience is good luck or bad and reminds us that a life marked by unbearable tragedy can still be meaningful.

                King’s ability to surprise, amaze, and bring us both terror and solace remains unsurpassed. Each of these stories holds its own thrills, joys, and mysteries; each feels iconic. You like it darker? You got it.''',
        isbn='978-1668037713',
        category='Science Fiction',
        image='https://m.media-amazon.com/images/I/71UTAmoNddL._SL1500_.jpg',
        publisher='Scribner',
        published_on=datetime.strptime("May 21, 2024", "%B %d, %Y"),
        rating=5.5,
        reviews=500
    ),
    Product(
        title='The Last House Guest',
        author='Megan Miranda',
        price=12.99,
        description='''A Reclusive heiress, a reformed con artist, and a charming new neighbor collide in this riveting tale of secrets, lies, and the search for a truth that may be hiding in plain sight.
        From the New York Times bestselling author of The Last Time I Lied and The Stranger Diaries comes a gripping new novel about a woman who must uncover the secrets of her own past in order to uncover the truth about her new neighbor.

        Ava is a reclusive heiress who has spent her life hiding from the world. She is a master of disguise and deception, but her latest neighbor may be the one person who can see through her facade.

        Lucas is a charming and handsome new neighbor who is hiding secrets of his own. He is a former con artist who has turned his life around, but his past is still shrouded in mystery.

        As Ava and Lucas get to know each other, they must navigate a web of lies and secrets that threaten to destroy their budding relationship. But as they dig deeper into each other's pasts, they may uncover a truth that is hiding in plain sight.

        The Last House Guest is a riveting tale of secrets, lies, and the search for truth that will keep you on the edge of your seat until the very end.''',
        isbn='978-1501144365',
        category='Science Fiction',
        image='https://m.media-amazon.com/images/I/815oQ6G6HDL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("June 1, 2020", "%B %d, %Y"),
        rating=4.5,
        reviews=250
    ),
    Product(
        title='The Maid',
        author='Nita Prose',
        price=14.99,
        description=''''A charming and riveting psychological thriller about a maid who becomes embroiled in a mystery at a luxurious hotel, from the New York Times bestselling author of The Silent Patient.
        Molly Gray is a maid at the Grand Regency Hotel, where she has worked for over a decade. She is a hard worker and takes great pride in her job, but she is also a bit of a loner.

        One day, Molly discovers the body of a wealthy guest in one of the hotel rooms. The police investigation that follows reveals that the guest was murdered, and Molly becomes the prime suspect.

        As Molly tries to clear her name, she uncovers a web of secrets and lies that threaten to destroy her life. She must navigate a complex cast of characters, including the hotel's wealthy and powerful guests, to uncover the truth about the murder.

        The Maid is a riveting psychological thriller about a woman who will stop at nothing to uncover the truth and clear her name. It is a must-read for fans of The Silent Patient and other psychological thrillers.''',
        isbn='978-1982168971',
        category='Science Fiction',
        image='https://m.media-amazon.com/images/I/719X2q+QV5L._SL1500_.jpg',
        publisher='Viking',
        published_on=datetime.strptime("January 4, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=200
    ),
    Product(
        title='The Paris Apartment',
        author='Lucy Foley',
        price=16.99,
        description=''''A riveting and atmospheric psychological thriller about a woman who discovers a dark secret in her friend's Paris apartment, from the New York Times bestselling author of The Guest List.
        Jess is a journalist who has just arrived in Paris to visit her friend, Ben. But when she arrives at his apartment, she finds it empty and a mysterious note that suggests Ben has disappeared.

        As Jess searches for Ben, she uncovers a dark secret about his past that threatens to destroy their friendship. She must navigate a complex cast of characters, including Ben's wealthy and powerful friends, to uncover the truth about his disappearance.

        The Paris Apartment is a riveting and atmospheric psychological thriller about a woman who will stop at nothing to uncover the truth about her friend's disappearance. It is a must-read for fans of The Guest List and other psychological thrillers.''',
        isbn='978-0062852583',
        category='Science Fiction',
        image='https://m.media-amazon.com/images/I/810PcNuumRL._SL1500_.jpg',
        publisher='William Morrow',
        published_on=datetime.strptime("February 22, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=150
    ),
    Product(
        title='The Last Thing He Told Me',
        author='Laura Dave',
        price=14.99,
        description='''A riveting and emotional psychological thriller about a woman who discovers a dark secret about her husband's past, from the New York Times bestselling author of Eight Hundred Grapes.
        Hannah Hall is a successful businesswoman who has it all - a loving husband, a beautiful home, and a fulfilling career. But when her husband disappears without a trace, Hannah's life is turned upside down.

        As she searches for her husband, Hannah uncovers a dark secret about his past that threatens to destroy their marriage. She must navigate a complex cast of characters, including her husband's mysterious colleagues and a detective who is determined to uncover the truth.

        The Last Thing He Told Me is a riveting and emotional psychological thriller about a woman who will stop at nothing to uncover the truth about her husband's disappearance. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1509840244',
        category='Science Fiction',
        image='https://m.media-amazon.com/images/I/81+TvkWc-uL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("May 4, 2021", "%B %d, %Y"),
        rating=4.5,
        reviews=300
    ),
    Product(
        title='The Silent Patient',
        author='Alex Michaelides',
        price=12.99,
        description='''A psychological thriller about a famous painter who shoots her husband and refuses to speak or cooperate with the police, and the psychotherapist who becomes obsessed with uncovering her secrets.
        Alicia Berenson is a famous painter who has it all - a loving husband, a beautiful home, and a successful career. But when she shoots her husband without warning, her life is turned upside down.

        Theo Faber is a psychotherapist who becomes obsessed with uncovering Alicia's secrets. As he delves deeper into her past, he uncovers a web of secrets and lies that threaten to destroy everything he thought he knew about her.

        The Silent Patient is a psychological thriller about a woman who will stop at nothing to keep her secrets buried. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1250301699',
        category='Science Fiction',
        image='https://m.media-amazon.com/images/I/71s6siGLrFL._SL1500_.jpg',
        publisher='Celadon Books',
        published_on=datetime.strptime("February 5, 2019", "%B %d, %Y"),
        rating=4.5,
        reviews=400
    ),
    # Add more products here
]

biography_books = [
    Product(
        title='You Like It Darker: Stories',
        author='Stephen King',
        price=18.90,
        description='''From legendary storyteller and master of short fiction Stephen King comes an extraordinary new collection of twelve short stories, many never-before-published, and some of his best EVER.

                “You like it darker? Fine, so do I,” writes Stephen King in the afterword to this magnificent new collection of twelve stories that delve into the darker part of life—both metaphorical and literal. King has, for half a century, been a master of the form, and these stories, about fate, mortality, luck, and the folds in reality where anything can happen, are as rich and riveting as his novels, both weighty in theme and a huge pleasure to read. King writes to feel “the exhilaration of leaving ordinary day-to-day life behind,” and in You Like It Darker, readers will feel that exhilaration too, again and again.

                “Two Talented Bastids” explores the long-hidden secret of how the eponymous gentlemen got their skills. In “Danny Coughlin’s Bad Dream,” a brief and unprecedented psychic flash upends dozens of lives, Danny’s most catastrophically. In “Rattlesnakes,” a sequel to Cujo, a grieving widower travels to Florida for respite and instead receives an unexpected inheritance—with major strings attached. In “The Dreamers,” a taciturn Vietnam vet answers a job ad and learns that there are some corners of the universe best left unexplored. “The Answer Man” asks if prescience is good luck or bad and reminds us that a life marked by unbearable tragedy can still be meaningful.

                King’s ability to surprise, amaze, and bring us both terror and solace remains unsurpassed. Each of these stories holds its own thrills, joys, and mysteries; each feels iconic. You like it darker? You got it.''',
        isbn='978-1668037713',
        category='Biography',
        image='https://m.media-amazon.com/images/I/71UTAmoNddL._SL1500_.jpg',
        publisher='Scribner',
        published_on=datetime.strptime("May 21, 2024", "%B %d, %Y"),
        rating=5.5,
        reviews=500
    ),
    Product(
        title='The Last House Guest',
        author='Megan Miranda',
        price=12.99,
        description='''A Reclusive heiress, a reformed con artist, and a charming new neighbor collide in this riveting tale of secrets, lies, and the search for a truth that may be hiding in plain sight.
        From the New York Times bestselling author of The Last Time I Lied and The Stranger Diaries comes a gripping new novel about a woman who must uncover the secrets of her own past in order to uncover the truth about her new neighbor.

        Ava is a reclusive heiress who has spent her life hiding from the world. She is a master of disguise and deception, but her latest neighbor may be the one person who can see through her facade.

        Lucas is a charming and handsome new neighbor who is hiding secrets of his own. He is a former con artist who has turned his life around, but his past is still shrouded in mystery.

        As Ava and Lucas get to know each other, they must navigate a web of lies and secrets that threaten to destroy their budding relationship. But as they dig deeper into each other's pasts, they may uncover a truth that is hiding in plain sight.

        The Last House Guest is a riveting tale of secrets, lies, and the search for truth that will keep you on the edge of your seat until the very end.''',
        isbn='978-1501144365',
        category='Biography',
        image='https://m.media-amazon.com/images/I/815oQ6G6HDL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("June 1, 2020", "%B %d, %Y"),
        rating=4.5,
        reviews=250
    ),
    Product(
        title='The Maid',
        author='Nita Prose',
        price=14.99,
        description=''''A charming and riveting psychological thriller about a maid who becomes embroiled in a mystery at a luxurious hotel, from the New York Times bestselling author of The Silent Patient.
        Molly Gray is a maid at the Grand Regency Hotel, where she has worked for over a decade. She is a hard worker and takes great pride in her job, but she is also a bit of a loner.

        One day, Molly discovers the body of a wealthy guest in one of the hotel rooms. The police investigation that follows reveals that the guest was murdered, and Molly becomes the prime suspect.

        As Molly tries to clear her name, she uncovers a web of secrets and lies that threaten to destroy her life. She must navigate a complex cast of characters, including the hotel's wealthy and powerful guests, to uncover the truth about the murder.

        The Maid is a riveting psychological thriller about a woman who will stop at nothing to uncover the truth and clear her name. It is a must-read for fans of The Silent Patient and other psychological thrillers.''',
        isbn='978-1982168971',
        category='Biography',
        image='https://m.media-amazon.com/images/I/719X2q+QV5L._SL1500_.jpg',
        publisher='Viking',
        published_on=datetime.strptime("January 4, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=200
    ),
    Product(
        title='The Paris Apartment',
        author='Lucy Foley',
        price=16.99,
        description=''''A riveting and atmospheric psychological thriller about a woman who discovers a dark secret in her friend's Paris apartment, from the New York Times bestselling author of The Guest List.
        Jess is a journalist who has just arrived in Paris to visit her friend, Ben. But when she arrives at his apartment, she finds it empty and a mysterious note that suggests Ben has disappeared.

        As Jess searches for Ben, she uncovers a dark secret about his past that threatens to destroy their friendship. She must navigate a complex cast of characters, including Ben's wealthy and powerful friends, to uncover the truth about his disappearance.

        The Paris Apartment is a riveting and atmospheric psychological thriller about a woman who will stop at nothing to uncover the truth about her friend's disappearance. It is a must-read for fans of The Guest List and other psychological thrillers.''',
        isbn='978-0062852583',
        category='Biography',
        image='https://m.media-amazon.com/images/I/810PcNuumRL._SL1500_.jpg',
        publisher='William Morrow',
        published_on=datetime.strptime("February 22, 2022", "%B %d, %Y"),
        rating=4.5,
        reviews=150
    ),
    Product(
        title='The Last Thing He Told Me',
        author='Laura Dave',
        price=14.99,
        description='''A riveting and emotional psychological thriller about a woman who discovers a dark secret about her husband's past, from the New York Times bestselling author of Eight Hundred Grapes.
        Hannah Hall is a successful businesswoman who has it all - a loving husband, a beautiful home, and a fulfilling career. But when her husband disappears without a trace, Hannah's life is turned upside down.

        As she searches for her husband, Hannah uncovers a dark secret about his past that threatens to destroy their marriage. She must navigate a complex cast of characters, including her husband's mysterious colleagues and a detective who is determined to uncover the truth.

        The Last Thing He Told Me is a riveting and emotional psychological thriller about a woman who will stop at nothing to uncover the truth about her husband's disappearance. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1509840244',
        category='Biography',
        image='https://m.media-amazon.com/images/I/81+TvkWc-uL._SL1500_.jpg',
        publisher='Simon & Schuster',
        published_on=datetime.strptime("May 4, 2021", "%B %d, %Y"),
        rating=4.5,
        reviews=300
    ),
    Product(
        title='The Silent Patient',
        author='Alex Michaelides',
        price=12.99,
        description='''A psychological thriller about a famous painter who shoots her husband and refuses to speak or cooperate with the police, and the psychotherapist who becomes obsessed with uncovering her secrets.
        Alicia Berenson is a famous painter who has it all - a loving husband, a beautiful home, and a successful career. But when she shoots her husband without warning, her life is turned upside down.

        Theo Faber is a psychotherapist who becomes obsessed with uncovering Alicia's secrets. As he delves deeper into her past, he uncovers a web of secrets and lies that threaten to destroy everything he thought he knew about her.

        The Silent Patient is a psychological thriller about a woman who will stop at nothing to keep her secrets buried. It is a must-read for fans of Gone Girl and other psychological thrillers.''',
        isbn='978-1250301699',
        category='Biography',
        image='https://m.media-amazon.com/images/I/71s6siGLrFL._SL1500_.jpg',
        publisher='Celadon Books',
        published_on=datetime.strptime("February 5, 2019", "%B %d, %Y"),
        rating=4.5,
        reviews=400
    ),
    # Add more products here
]

def add_books_to_db():
    for book in fiction_books:
        db.session.add(book)

    for book in non_fiction_books:
        db.session.add(book)

    for book in si_fi_books:
        db.session.add(book)

    for book in biography_books:
        db.session.add(book)

    db.session.commit()

with app.app_context():
    db.drop_all()
    db.create_all()
    add_books_to_db()

if __name__ == '__main__':
    app.run(debug=True)
