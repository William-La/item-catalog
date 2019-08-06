#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import jsonify, make_response, session as login_session
from flask_httpauth import HTTPBasicAuth
from google.oauth2 import id_token
from google.auth.transport import requests
import json

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///itemCatalog.db',
                       connect_args={'check_same_thread': False})

# create database session
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

PROVIDERS = ['accounts.google.com', 'https://accounts.google.com']

# *** Login and User Auth Functions ***
try:
    JSON_DATA = json.loads(open('client_secrets.json', 'r').read())['web']
    CLIENT_ID = JSON_DATA['client_id']
    CLIENT_SECRET = JSON_DATA['client_secret']
except ValueError:
    print('*** ERROR: Could not find \'client_secrets.json\' file ***')


# anti-forgery state token w/ Google sign-in
def callback_auth():
    # Google sign-in API guidelines:
    # https://developers.google.com/identity/sign-in/web/sign-in
    try:
        if "idtoken" in request.form:
            # User is trying to log in
            # if user is already logged in
            if "user" in login_session:
                return_msg = make_response(jsonify(
                             message="User is logged in.", status=201))
            # else user is not logged in
            else:
                token = request.form['idtoken']
                # verify the JWT, client ID, and that the token has not expired
                idinfo = id_token.verify_oauth2_token(
                         token, requests.Request(), CLIENT_ID)
                # verify the issuer of the ID token
                if idinfo['iss'] not in PROVIDERS:
                    raise ValueError("Wrong Issuer")
                # ID token is valid, can get info from decoded token
                userid = idinfo['sub']
                # add to session
                login_session['user'] = token
                login_session['userid'] = userid

                return_msg = make_response(jsonify(
                             message='Logged in Successfully', status=200))

        else:
            # if user is logged in, log them out
            if 'user' in login_session:
                del login_session['user']
                del login_session['userid']
                return_msg = make_response(jsonify(
                             message="Logged out Successfully", status=200))
    # if token invalid
    except ValueError:
        return_msg = make_response(jsonify(
                     message="Could not verify token", status=400))

    return_msg.headers['Content-Type'] = 'application/json'
    return return_msg


# *** Route declarations and functionality ***
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
        # flash('Item Successfully Added')
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
        # flash('Item Successfully Edited')
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
        # flash('Item Successfully Deleted')
        return redirect(url_for('landingPage'))
    else:
        return render_template("delete.html", item=item)


# JSON function
@app.route("/catalog.json")
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
