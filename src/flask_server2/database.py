from flask import Flask, request, render_template, jsonify, redirect
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy

#  - - - - - - - Defaults - - - - - - - #
""" 
Machine specific settings
    By default the machine should load from the settings to determine the machine state. 
    The inputs are only to change if needed on startup. 
    It should check if ./temp/settings.json exists
    If not it should create it with default settings. 
    This should not be sent to gitlab, only stored locally 
"""

app = Flask(__name__)

#  - - - - - - - Database Config and Initialization- - - - - - - #
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1:3306/circuitprinter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


from sqlalchemy.types import JSON
from sqlalchemy.ext.mutable import MutableDict
# Base = declarative_base()


class Project(db.Model):
    """
    A project contains:
        (string) name,
        (list) sequential instances of Process
    """
    # __tablename__ = 'projects'
    name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    settings = db.Column(MutableDict.as_mutable(JSON), nullable=True)

    # slug = db.Column(db.String(100))

    # def __init__(self, name):
    #     self.name = name
    #     self.slug = '-'.join(name.split()).lower()

    def __rep__(self):
        return '<Project %r>' % self.name


class Recipe(db.Model):
    """
    A recipe contains: 
        (string) process_type
        (dict) process_parameters: allowable parmeters would be: 
            on_delay
            off_delay
            retract_height 
    """
    name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    process_types = ['extrusion_silver_print', 'adhesive_dispense', 'cure','pick_and_place', 'inspect'] 

    def __repr__(self) -> str:
        return '<Recipe %r>' % self.name 


class Tool(db.Model):
    """
    A tool contains: 
        (string) name: name of the tool 
        (class) actions: possible actions the tool can take 
    """
    name = db.Column(db.String(200))
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self) -> str:
        return '<Tool %r>' % self.name 


class Process(db.Model):
    """
    A process contains: 
        (class) Tool: 
        (class) Recipe: 
        (string) name: 
        (string) artwork_path: path to unparsed artwork file, dxf, gerber, etc 
        (list) artwork: 
    """
    name = db.Column(db.String(200))
    id = db.Column(db.Integer, primary_key=True)
    artwork_path = db.Column(db.String(500)) 
    
    def __init__(self, name, artwork_path):
        self.name = name 
        self.artwork_path = artwork_path

    def __repr__(self) -> str:
        return '<Process %r>' % self.name 

