"""
Nathan Pretorius 2022
"""

from collections import defaultdict
from flask import Flask, request, render_template, jsonify, redirect
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy

#from sqlalchemy.orm import declarative_base
#from SQLAlchemy import Column, Integer, String, DateTime
import glob, os 
import json
import threading


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Base = declarative_base()


class Project(db.Model):
    """
    A project contains:
        (string) name, 
        (list) sequential instances of Process 
    """
    #__tablename__ = 'projects'
    name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    #slug = db.Column(db.String(100)) 

    # def __init__(self, name):
    #     self.name = name
    #     self.slug = '-'.join(name.split()).lower()
    
    def __rep__(self):
        return '<Project %r>' % self.name


@app.route("/")
def home():
    return render_template('home.html')

def startup():
    pass

# = = = = = = = = Projects CRUD = = = = = = = = # 
@app.route("/projects", methods=["GET","POST"])
def projects():
    # = = = = = = = Create = = = = = = = #
    if request.method == "POST":
        project_content = request.form['content'] 
        new_project = Project(content=project_content) 

        try: 
            db.session.add(new_project) 
            db.session.commit() 
            return redirect('/projects') 
        except:
            return 'There was an error while adding the project' 
    else:
        # = = = = = = = Read = = = = = = = #
        projects = Project.query.all()
        return render_template("projects.html", projects=projects)

@app.route('/delete/<int:id>')
def delete(id):
    # = = = = = = = Delete = = = = = = = #
    project_to_delete = Project.query.get_or_404(id)
    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/projects')
    except:
        return 'There was an error while deleting that project'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    # = = = = = = = Update = = = = = = = #
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/projects')
        except:
            return 'There was an issue while updating that project'

    else:
        return render_template('update.html', project=project)


# # = = = = = = = = Process CRUD = = = = = = = = # 
# @app.route("/<str:project_name>/list_processes", methods=["GET", "POST"]) 
# def processes():
#     # = = = = = = = Add new process = = = = = = = #
#     if request.method == "POST":
#         process_type = request.form['process_type'] 
#         process_name = request.form['process_name'] 
#         process_file = request.form['process_file'] 
#         new_process = Process(name=process_name,process_type=process_type, process_file=process_file) 

#         try:
#             db.session.add(new_process)
#             db.session.commit()
#             return redirect('/<str:project_name>/list_processes')
#         except:
#             return 'There was an error while adding the process'
#     else:
#         # = = = = = = = Read = = = = = = = #
#         projects = Project.query.all()
#         return render_template("/<str:project_name>/list_processes.html", processes=processes) 

# @app.route('/list_processes', methods=['GET','POST'])
# def list_processes(): 
#     processes = ['extrusion_print', 'cure', 'pick_and_place']
#     if request.method == 'POST':
#         return render_template('/list_processes') 
#     else:
#         return render_template('/list_processes', processes=processes) 

@app.route("/settings", methods={"GET", "POST"}) 
def settings():
    if request.method == "POST":
        pass
    else:
        return render_template('settings.html') 

@app.route("/calibrate", methods={"GET", "POST"}) 
def calibrate():
    if request.method == "POST":
        pass
    else:
        return render_template('calibrate.html') 


if __name__ == "__main__":
    app.run(debug=True) 