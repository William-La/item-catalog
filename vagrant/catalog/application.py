
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import session as login_session
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///itemCatalog.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
