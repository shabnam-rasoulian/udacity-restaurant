from flask import flash, Flask, jsonify, request, redirect, render_template, url_for
app = Flask(__name__)

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/")
@app.route("/restaurants")
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants = restaurants)

@app.route("/restaurants/JSON")
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])

@app.route("/restaurant/new", methods = ["GET", "POST"])
def newRestaurant():
    if request.method == "POST":
        restaurant = Restaurant(name = request.form["name"])
        session.add(restaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for("showRestaurants"))
    else:
        return render_template("newrestaurant.html")

@app.route("/restaurant/<int:restaurant_id>/edit", methods = ["GET", "POST"])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == "POST":
        restaurant.name = request.form["name"]
        session.add(restaurant)
        session.commit()
        flash("Restaurant Successfully Edited!")
        return redirect(url_for("showRestaurants"))
    else:
        return render_template("editrestaurant.html", restaurant_id = restaurant_id, restaurant = restaurant)

@app.route("/restaurant/<int:restaurant_id>/delete", methods = ["GET", "POST"])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == "POST":
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Successfully Deleted!")
        return redirect(url_for("showRestaurants"))
    else:
        return render_template("deleterestaurant.html", restaurant = restaurant)

@app.route("/restaurant/<int:restaurant_id>")
@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    appetizers = []
    entrees = []
    desserts = []
    beverages = []
    for item in items:
        if item.course == "Appetizer":
            appetizers.append(item)
        elif item.course == "Entree":
            entrees.append(item)
        elif item.course == "Dessert":
            desserts.append(item)
        elif item.course == "Beverage":
            beverages.append(item)
    return render_template("menu.html", restaurant = restaurant, items = items, appetizers = appetizers, entrees = entrees, desserts = desserts, beverages = beverages)


@app.route("/restaurant/<int:restaurant_id>/menu/JSON")
def showMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [item.serialize for item in items])

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def showMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = [item.serialize])

@app.route("/restaurant/<int:restaurant_id>/menu/new", methods = ["GET", "POST"])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == "POST":
        menuItem = MenuItem(name = request.form["name"], description = request.form["description"], price = request.form["price"], course = request.form["course"], restaurant_id = restaurant_id)
        session.add(menuItem)
        session.commit()
        flash("Menu item Created!")
        return redirect(url_for("showMenu", restaurant_id = restaurant_id))
    else:
        return render_template("newmenuitem.html", restaurant = restaurant)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit", methods = ["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        if request.form["name"]:
            item.name = request.form["name"]
        if request.form["description"]:
            item.description = request.form["description"]
        if request.form["price"]:
            item.price = request.form["price"]
        if request.form["course"]:
            item.course = request.form["course"]
        session.add(item)
        session.commit()
        flash("Menu Item Successfully Edited!")
        return redirect(url_for("showMenu", restaurant_id = restaurant_id))
    else:
        return render_template("editmenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, item = item)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete", methods = ["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("Menu Item Seccessfully Deleted!")
        return redirect(url_for("showMenu", restaurant_id = restaurant_id))
    else:
        return render_template("deletemenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, item = item)

if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
