#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import jsonify, session as login_session
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///itemCatalog.db',
                       connect_args={'check_same_thread': False})

# create database session
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# route declarations and functionality
# route for landing page and recent items
@app.route("/")
def landingPage():
    recentItems = session.query(Item).order_by(Item.id.desc())[0:8]
    return render_template('landing.html', recentItems=recentItems)


# route for showing the items in a category
@app.route("/catalog/<category>")
@app.route("/catalog/<category>/items")
def showCategory(category):
    cat_id = session.query(Category).filter_by(name=category).first().id
    items = session.query(Item).filter_by(cat_id=cat_id).all()
    return render_template("category.html", items=items, category=category)


# route for showing an item and its description
@app.route("/catalog/<category>/<itemTitle>")
def showItem(category, itemTitle):
    cat_id = session.query(Category).filter_by(name=category).first().id
    item = session.query(Item).filter_by(
           cat_id=cat_id, title=itemTitle).first()
    return render_template("item.html", item=item)


# route for creating a new item (requires login)
@app.route("/catalog/new", methods=['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        title = ""
        desc = ""
        if request.form['title']:
            title = request.form['title']
        if request.form['desc']:
            desc = request.form['desc']
        if request.form['category']:
            name = request.form['category']
            category = session.query(Category).filter_by(name=name).first()
        newItem = Item(category=category, title=title, desc=desc)
        session.add(newItem)
        session.commit()
        #flash('Item Successfully Added')
        return redirect(url_for('landingPage'))
    else:
        return render_template("new.html")


# route for editing an item (requires login)
@app.route("/catalog/<itemTitle>/edit", methods=['GET', 'POST'])
def editItem(itemTitle):
    item = session.query(Item).filter_by(title=itemTitle).first()
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['desc']:
            item.desc = request.form['desc']
        if request.form['category']:
            new_cat = session.query(Category).filter_by(
                         name=request.form['category']).first()
            item.category = new_cat
        session.add(item)
        session.commit()
        #flash('Item Successfully Edited')
        return redirect(url_for('showCategory', category=item.category.name))
    else:
        return render_template("edit.html", item=item)


# route for deleting an item (requires login)
@app.route("/catalog/<itemTitle>/delete", methods=['GET', 'POST'])
def deleteItem(itemTitle):
    item = session.query(Item).filter_by(title=itemTitle).first()
    category = item.category.name
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        #flash('Item Successfully Deleted')
        return redirect(url_for('landingPage'))
    else:
        return render_template("delete.html", item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
