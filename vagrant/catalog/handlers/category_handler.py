from flask import request, redirect, url_for, jsonify, flash
from flask import session as login_session
from sqlalchemy import asc, desc

from utils import app, session, render, user_logged_in, category_exists, user_owns_category, valid_category
from models import Category, Item


@app.route('/catalog/')
def show_categories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render('showcategories.html', categories=categories)


@app.route('/catalog/JSON')
def categories_json():
    categories = session.query(Category).order_by(asc(Category.name))
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/catalog/newcat/', methods=['GET', 'POST'])
@user_logged_in
def new_category():
    if request.method == 'GET':
        return render('newcategory.html')

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if valid_category(name, description):
            user_id = login_session['user_id']
            category = Category(name=name, description=description, user_id=user_id)
            session.add(category)
            session.commit()
            flash("Newed category %s!" % category.name)
            return redirect(url_for("show_items", category_id=category.id))
        else:
            error = "Complete info please!"
            return render('newcategory.html', name=name, description=description, error=error)


@app.route('/catalog/<int:category_id>/editcat/', methods=['GET', 'POST'])
@user_logged_in
@category_exists
@user_owns_category
def edit_category(category):
    if request.method == 'GET':
        return render('editcategory.html', category=category, name=category.name,
                      description=category.description)
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if valid_category(name, description):
            category.name = name
            category.description = description
            session.commit()
            flash("Edited category %s!" % category.name)
            return redirect(url_for("show_items", category_id=category.id))
        else:
            error = "Complete info please!"
            return render('editcategory.html', category=category, name=name, description=description, error=error)


@app.route('/catalog/<int:category_id>/deletecat/', methods=['GET', 'POST'])
@user_logged_in
@category_exists
@user_owns_category
def delete_category(category):
    if request.method == 'GET':
        return render('deletecategory.html', category=category)
    elif request.method == 'POST':
        items = category.items
        if items:
            for item in items:
                session.delete(item)
        session.delete(category)
        session.commit()
        flash("Deleted category %s!" % category.name)
        return redirect(url_for('show_categories'))


@app.route('/catalog/<int:category_id>/items/')
@category_exists
def show_items(category):
    items = session.query(Item).filter_by(category_id=category.id).order_by(desc(Item.created_at))
    return render('showitems.html', category=category, items=items)


@app.route('/catalog/<int:category_id>/items/JSON')
@category_exists
def items_json(category):
    items = sorted(category.items, key=lambda i: i.created_at, reverse=True)
    return jsonify(Category=category.serialize, Items=[i.serialize for i in items])
