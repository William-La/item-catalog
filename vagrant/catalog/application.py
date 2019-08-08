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


# verifying user session

# anti-forgery state token w/ Google sign-in
@app.route("/googleoauth", methods=['POST'])
def callback_oauth():
    # Google sign-in API guidelines:
    # https://developers.google.com/identity/sign-in/web/sign-in
    try:
        if 'idtoken' in request.form:
            # User is trying to log in
            # if user is already logged in
            if 'token' in login_session:
                print 'logged in'
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
                
                # check if user is in the db
                userdb = session.query(User).filter_by(id=userid).first()
                # if user is not in the db, create new user
                if not userdb:
                    
                    email = idinfo['email']
                    userdb = User(id=userid, email=email)
                    session.add(userdb)
                    session.commit()
                    # flash('New user created!')
                # if user is in the db
                else:
                    print('WIP because flash not implemented yet')
                    # flash('User logged in!')
                # add to session
                print 'what'
                login_session['token'] = userdb.gen_auth_token()
                login_session['user'] = token
                login_session['userid'] = userid
                
                return login_session.get('token', None)

        elif 'token' in login_session:
            print('signout')
            # if user is logged in, log them out
            g.current_user = None
            login_session.pop('token', None)
            login_session.pop('user', None)
            login_session.pop('userid', None)
            return 'logged out'
    # if token invalid
    except ValueError:
        pass
        #return_msg = '*** ERROR: invalid token ***'

    return redirect(url_for('landingPage'))


# *** Route declarations and functionality ***
# route for landing page and recent items
@app.route("/")
def landingPage():
    user = None
    if 'token' in login_session:
        print("there is a user!")
        user = User.verify_auth_token(login_session['token'])
    recentItems = session.query(Item).order_by(Item.id.desc())[0:8]
    return render_template('landing.html', recentItems=recentItems, user=user,
           CLIENT_ID=CLIENT_ID)


# route for showing the items in a category
@app.route("/catalog/<category>")
@app.route("/catalog/<category>/items")
def showCategory(category):
    cat_id = session.query(Category).filter_by(name=category).first().id
    items = session.query(Item).filter_by(cat_id=cat_id).all()
    return render_template("category.html", items=items, category=category,
           CLIENT_ID=CLIENT_ID)


# route for showing an item and its description
@app.route("/catalog/<category>/<itemTitle>")
def showItem(category, itemTitle):
    user = None
    if 'token' in login_session:
        user = User.verify_auth_token(login_session['token'])
    cat_id = session.query(Category).filter_by(name=category).first().id
    item = session.query(Item).filter_by(
           cat_id=cat_id, title=itemTitle).first()
    return render_template("item.html", item=item, user=user,
           CLIENT_ID=CLIENT_ID)


# route for creating a new item (requires login)
@app.route("/catalog/new", methods=['GET', 'POST'])
def newItem():
    if 'token' not in login_session:
        # flash('Unauthorized. Please log in.')
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
        newItem = Item(category=category, title=title, desc=desc)
        session.add(newItem)
        session.commit()
        # flash('Item Successfully Added')
        return redirect(url_for('landingPage'))
    # else the user is trying to create a new item
    else:
        return render_template("new.html", CLIENT_ID=CLIENT_ID)


# route for editing an item (requires login)
@app.route("/catalog/<itemTitle>/edit", methods=['GET', 'POST'])
def editItem(itemTitle):
    item = session.query(Item).filter_by(title=itemTitle).first()
    if 'token' not in login_session:
        # flash('Unauthorized. Please log in.')
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
        # flash('Item Successfully Edited')
        return redirect(url_for('showCategory', category=item.category.name))
    # else the user is going to edit
    else:
        return render_template("edit.html", item=item, CLIENT_ID=CLIENT_ID)


# route for deleting an item (requires login)
@app.route("/catalog/<itemTitle>/delete", methods=['GET', 'POST'])
def deleteItem(itemTitle):
    item = session.query(Item).filter_by(title=itemTitle).first()
    category = item.category.name
    if 'token' not in login_session:
        # flash('Unauthorized. Please log in.')
        return redirect(url_for('landingPage'))
    # if the user has deleted the item
    elif request.method == 'POST':
        session.delete(item)
        session.commit()
        # flash('Item Successfully Deleted')
        return redirect(url_for('landingPage'))
    # else the user is going to delete
    else:
        return render_template("delete.html", item=item, CLIENT_ID=CLIENT_ID)


# JSON endpoint function
@app.route("/catalog.json")
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[c.serialize for c in categories])


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
