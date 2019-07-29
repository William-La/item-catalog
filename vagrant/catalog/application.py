from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import jsonify, session as login_session
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///itemCatalog.db',
                       connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route("/")
def landingPage():
    recentItems = session.query(Item).order_by(Item.id)[0:9]
    return render_template('landing.html', recentItems=recentItems)


@app.route("/catalog/<String: category>/items")
def showCategory(category):
    cat_id = session.query(Category).filter_by(name=category).first().id
    items = sesison.query(Item).filter_by(cat_id=cat_id).all
    return render_template("category.html", items=items)


@app.route("/catalog/(String: category>/<String: itemTitle>")
def showItem(category, itemTitle):
    cat_id = session.query(Category).filter_by(name=category).first().id
    item = session.query(Item).filter_by(
           cat_id=cat_id, title=itemTitle).first()
    return render_template("item.html", item=item)


@app.route("/catalog/<String: itemTitle>/edit", methods=['GET', 'POST'])
def editItem(itemTitle):
    item = session.query(Item).filter_by(title=itemTitle).first()
    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['desc']:
            item.desc = request.form['desc']
        if request.form['category']:
            new_cat_id = session.query(Category).filter_by(
                         name=request.form['category']).first().id
            item.cat_id = new_cat_id
            item.category = request.form['category']
        session.add(item)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showCategory', category=item.category))
    else:
        return render_template("edit.html", item=item)


@app.route("/catalog/<String: itemTitle>/delete", methods=['GET', 'POST'])
def deleteItem(itemTitle):
    item = session.query(Item).filter_by(title=itemTitle).first()
    category = item.category.name
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCategory', category=category))
    else:
        return render_template("delete.html", item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
