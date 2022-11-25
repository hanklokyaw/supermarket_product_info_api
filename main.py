from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_category = db.Column(db.String(250), nullable=False)
    sub_category = db.Column(db.String(500), nullable=False)
    item_name = db.Column(db.String(500), nullable=False)
    price = db.Column(db.String(250), nullable=True)
    ingredients = db.Column(db.String(250), nullable=True)
    brand = db.Column(db.String(250), nullable=True)
    serving_size = db.Column(db.String(250), nullable=True)
    calories = db.Column(db.String(250), nullable=True)
    total_fat = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all")
def get_all_products():
    products = db.session.query(Product).all()
    # This uses a List Comprehension but you could also split it into 3 lines.
    return jsonify(products=[product.to_dict() for product in products])


@app.route("/search")
def get_product_by_id():
    query_id = request.args.get("id")
    id = db.session.query(Product).filter_by(id=query_id).first()
    if id:
        return jsonify(products=id.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a category with that name."})



@app.route("/add", methods=["POST"])
def post_new_product():
    new_product = Product(
        id=request.form.get("id"),
        main_category=request.form.get("main_category"),
        sub_category=request.form.get("sub_category"),
        item_name=request.form.get("item_name"),
        price=request.form.get("price"),
        ingredients=request.form.get("ingredients"),
        brand=request.form.get("brand"),
        serving_size=request.form.get("serving_size"),
        calories=request.form.get("calories"),
        total_fat=request.form.get("total_fat")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new product."})


@app.route("/random")
def get_random_product():
    product = db.session.query(Product).all()
    random_product = random.choice(product)
    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(products=random_product.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
