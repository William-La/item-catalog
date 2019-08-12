#!/usr/bin/env python
from flask import Flask, g, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import jsonify, make_response, session as login_session
from flask_httpauth import HTTPTokenAuth
from google.oauth2 import id_token
from google.auth.transport import requests
import json

auth = HTTPTokenAuth(scheme="Token")


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
@app.route("/googleoauth", methods=['POST'])
def callback_oauth():
    """connect Google sign-in to backend auth"""

    # Google sign-in API guidelines:
    # https://developers.google.com/identity/sign-in/web/sign-in
    try:
        # if user is trying to log in
        if 'idtoken' in request.form:
            # if user is already logged in
            if 'token' in login_session:
                return login_session.get('token', None)
            # else user is not logged in
            else:
                token = request.form['idtoken']

                # verify the JWT, client ID, and that the token has not expired
                idinfo = id_token.verify_oauth2_token(token,
                                                      requests.Request(),
                                                      CLIENT_ID)

                # verify the issuer of the ID token
                if idinfo['iss'] not in PROVIDERS:
                    raise ValueError("Wrong Issuer")

                # ID token is valid, can get info from decoded token
                userid = idinfo['sub']
                email = idinfo['email']
                # check if user is in the db
                userdb = session.query(User).filter_by(id=userid).first()
                # if user is not in the db, create new user
                if not userdb:
                    # create a new db user
                    userdb = User(id=userid, email=email)
                    session.add(userdb)
                    session.commit()
                    flash('New user created!')
                # else if user is already in the db
                else:
                    flash('User logged in!')
                # add to session
                login_session['token'] = userdb.gen_auth_token()
                login_session['user'] = token
                login_session['userid'] = userid
                login_session['email'] = email

                return login_session.get('token', None)

        elif 'token' in login_session:
            # if user is logged in, log them out
            g.current_user = None
            login_session.pop('token', None)
            login_session.pop('user', None)
            login_session.pop('userid', None)
            flash('User signed out')
            return 'logged out'
    # if token invalid
    except ValueError:
        pass

    return redirect(url_for('landingPage'))


# *** Route declarations and functionality ***
# route for landing page and recent items
@app.route("/")
def landingPage():
    """landing page displays items recently added to the db"""

    user = None
    # if a user is logged in, then 'token' will be in login session
    if 'token' in login_session:
        # verify the user
        user = User.verify_auth_token(login_session['token'])
    recentItems = session.query(Item).order_by(Item.id.desc())[0:8]
    # pass the user parameter to determine if 'add new item' and 'signout'
    # button is shown
    return render_template('landing.html', recentItems=recentItems, user=user,
                           CLIENT_ID=CLIENT_ID)


# route for showing the items in a category
@app.route("/catalog/<category>")
def showCategory(category):
    """displays the items listed under a specific category"""

    # if a user is logged in, then 'token' will be in login session
    user = None
    if 'token' in login_session:
        # verify the user
        user = User.verify_auth_token(login_session['token'])
    cat_id = session.query(Category).filter_by(name=category).first().id
    items = session.query(Item).filter_by(cat_id=cat_id).all()
    # pass the user parameter to determine if 'signout' button is shown
    return render_template("category.html", items=items, category=category,
                           user=user, CLIENT_ID=CLIENT_ID)


# route for showing an item and its description
@app.route("/catalog/<category>/<itemTitle>")
def showItem(category, itemTitle):
    """shows the profile of a specific item"""

    user = None
    # if a user is logged in, then 'token' will be in login session
    if 'token' in login_session:
        user = User.verify_auth_token(login_session['token'])
    cat_id = session.query(Category).filter_by(name=category).first().id
    item = session.query(Item).filter_by(
           cat_id=cat_id, title=itemTitle).first()
    # if there is a user, check if they're the item's creator (Authorization)
    if user:
        # if item's credentials do not match up with user's, prevent editing
        if item.creator_id != login_session['userid'] or item.creator_email != login_session['email']:
            user = None
            flash("Not authorized to edit or delete this item.")

    # pass the user parameter to determine if 'edit', 'delete', and 'signout'
    # button is shown
    return render_template("item.html", item=item, user=user,
                           CLIENT_ID=CLIENT_ID)


# route for creating a new item (requires login)
@app.route("/catalog/new", methods=['GET', 'POST'])
def newItem():
    """allows authenticated users to add new items to the catalog"""

    # redirect if user is not logged in
    if 'token' not in login_session:
        flash('Unauthorized. Please log in.')
        return redirect(url_for('landingPage'))
    # if the user has created a new item
    elif request.method == 'POST':
        title = ""
        desc = ""
        if request.form['title']:
            title = request.form['title']
        if request.form['desc']:
            desc = request.form['desc']
        if request.form['category']:
            name = request.form['category']
            category = session.query(Category).filter_by(name=name).first()
        email = login_session['email']
        userid = login_session['userid']
        newItem = Item(category=category, title=title, desc=desc,
                       creator_id=userid, creator_email=email)
        session.add(newItem)
        session.commit()
        flash('Item Successfully Added')
        return redirect(url_for('landingPage'))
    # else the user is trying to create a new item
    else:
        return render_template("new.html", CLIENT_ID=CLIENT_ID)


# route for editing an item (requires login)
@app.route("/catalog/<itemTitle>/edit", methods=['GET', 'POST'])
def editItem(itemTitle):
    """allows authenticated users to edit items in the catalog"""

    item = session.query(Item).filter_by(title=itemTitle).first()
    # redirect if user is not logged in
    if 'token' not in login_session:
        flash('Unauthorized. Please log in.')
        return redirect(url_for('landingPage'))
    # Authorization check
    elif item.creator_id != login_session['userid'] or item.creator_email != login_session['email']:
         flash('Not authorized to edit that item.')
         return redirect(url_for('landingPage'))
    # if the user has edited the item
    elif request.method == 'POST':
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
        flash('Item Successfully Edited')
        return redirect(url_for('showCategory', category=item.category.name))
    # else the user is going to edit
    else:
        return render_template("edit.html", item=item, CLIENT_ID=CLIENT_ID)


# route for deleting an item (requires login)
@app.route("/catalog/<itemTitle>/delete", methods=['GET', 'POST'])
def deleteItem(itemTitle):
    """allows authenticated users to delete items"""

    item = session.query(Item).filter_by(title=itemTitle).first()
    category = item.category.name
    # redirect if user is not logged in
    if 'token' not in login_session:
        flash('Unauthorized. Please log in.')
        return redirect(url_for('landingPage'))
    # Authorization check
    elif item.creator_id != login_session['userid'] or item.creator_email != login_session['email']:
         flash('Not authorized to delete that item.')
         return redirect(url_for('landingPage'))
    # if the user has deleted the item
    elif request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('landingPage'))
    # else the user is going to delete
    else:
        return render_template("delete.html", item=item, CLIENT_ID=CLIENT_ID)


# JSON endpoint for entire catalog
@app.route("/json")
@app.route("/catalog/json")
def catalogJSON():
    categories = session.query(Category).all()
    if categories:
        return jsonify(Catalog=[c.serialize for c in categories])
    else:
        return jsonify({"Message": "Error, please fill database"})

# JSON endpoint for single category
@app.route("/catalog/<category>/json")
def categoryJSON(category):
    cat = session.query(Category).filter_by(name=category).first()
    if cat:
        return jsonify(Category=cat.serialize)
    else:
        return jsonify({'Message': "Category not found"})

# JSON endpoint for single item
@app.route("/catalog/<category>/<itemTitle>/json")
def itemJSON(category, itemTitle):
    cat = session.query(Category).filter_by(name=category).first()
    if cat:
        item = session.query(Item).filter_by(
               title=itemTitle, cat_id=cat.id).first()
        if item:
            return jsonify(Item=item.serialize)
        else:
            return jsonify({"Message": "Item not found"})
    else:
        return jsonify({"Message": "Category not found"})


if __name__ == '__main__':
    # change to secure secret key if going to production site
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
