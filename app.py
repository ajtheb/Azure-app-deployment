import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine, text

id = 1
app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import Products

@app.route('/', methods=['GET'])
def index():
    print('Getting all products')
    products = Products.query.all()
    
    return render_template('index.html', products=products)

# @app.route('/<int:id>', methods=['GET'])
# def details(id):
    
#     return render_template('details.html', restaurant=restaurant, reviews=reviews)

# @app.route('/create', methods=['GET'])
# def create_restaurant():
#     print('Request for add restaurant page received')
#     return render_template('create_restaurant.html')

@app.route('/saveData', methods=['POST'])
@csrf.exempt
def add_product():
    try:
        name = request.values.get('name')
        category = request.values.get('category')
        brand = request.values.get('brand')
        qty = request.values.get('qty')
        price = request.values.get('price')
        print(name,category,brand)
    except (KeyError):
        # Redisplay the question voting form.
        return render_template('add_restaurant.html', {
            'error_message': "You must include a restaurant name, address, and description",
        })
    else:
        cur_products = Products.query.all()
        id=1
        for p in cur_products:
            if p.id:
                id = max(id,p.id)+1

        product = Products()
        product.id = id
        product.name = name
        product.category = category
        product.brand = brand
        product.qty = int(qty)
        product.price = int(price)
        db.session.add(product)
        db.session.commit()
    return redirect('/')

# @app.route('/review/<int:id>', methods=['POST'])
# @csrf.exempt
# def add_review(id):
#     try:
#         user_name = request.values.get('user_name')
#         rating = request.values.get('rating')
#         review_text = request.values.get('review_text')
#     except (KeyError):
#         #Redisplay the question voting form.
#         return render_template('add_review.html', {
#             'error_message': "Error adding review",
#         })
#     else:
#         review = Review()
#         review.restaurant = id
#         review.review_date = datetime.now()
#         review.user_name = user_name
#         review.rating = int(rating)
#         review.review_text = review_text
#         db.session.add(review)
#         db.session.commit()

#     return redirect(url_for('details', id=id))

# @app.context_processor
# def utility_processor():
#     def star_rating(id):
#         reviews = Review.query.where(Review.restaurant == id)

#         ratings = []
#         review_count = 0
#         for review in reviews:
#             ratings += [review.rating]
#             review_count += 1

#         avg_rating = sum(ratings) / len(ratings) if ratings else 0
#         stars_percent = round((avg_rating / 5.0) * 100) if review_count > 0 else 0
#         return {'avg_rating': avg_rating, 'review_count': review_count, 'stars_percent': stars_percent}

#     return dict(star_rating=star_rating)

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
