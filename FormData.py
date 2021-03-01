import sqlite3
from flask import Flask, redirect, request, url_for,render_template
import requests
from flask_sqlalchemy import SQLAlchemy
from app import database as db


# class Application(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     fname=db.Column(db.String(50), nullable=False)
#     lname=db.Column(db.String(50), nullable=False)
#     r_n=db.Column(db.String(200), nullable=False)
#     phone_number=db.column(db.Integer,nullable=False)
#     gender=db.Column(db.String(12), nullable=False)
#     age=db.column(db.Integer,nullable=False)
#     city=db.Column(db.String(24), nullable=False)
#     state=db.Column(db.String(24), nullable=False)
#     programme=db.Column(db.String(24), nullable=False)
#     year=db.Column(db.Integer, nullable=False)
#     branch=db.Column(db.String(12), nullable=False)
#     travel_mode=db.Column(db.String(12), nullable=False)
#     cllg_equip=db.Column(db.String(24), nullable=False)
#     symptoms=db.Column(db.String(24), nullable=False)
#     rtd=db.Column(db.String(24), nullable=False)
#     description=db.Column(db.String(300), nullable=False)
#     happiness=db.Column(db.String(12), nullable=False)
    
#     def __repr__(self):
#         return '<Application %r>' % self.id

