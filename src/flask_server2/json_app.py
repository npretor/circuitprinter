"""
Nathan Pretorius 2022
"""

from collections import defaultdict
from concurrent.futures import process
from platform import machine
from flask import Flask, request, render_template, jsonify, redirect
from flask.views import View, MethodView
from flask_sqlalchemy import SQLAlchemy

#from sqlalchemy.orm import declarative_base
#from SQLAlchemy import Column, Integer, String, DateTime
import glob, os 
import json
import threading
import uuid


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

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/list_processes') 
def list_processes():
    """
    JSON define process list for now 
    Move to SQL after the UI is working fully 
    """
    with open('../config/processes.json','r') as f:
        process_data = json.load(f) 
    
    processes = process_data["processes"].copy()

    return render_template('list_processes.html', processes=processes)

@app.route('/create_process', methods=["GET","POST"]) 
def create_process():   
    if request.method == "POST":  
        # project_name, file, project_type, ink_recipe
        project_name = request.form['project_name']
        file_path = request.form['filename']
        process_type = request.form['process_type']
        ink_recipe = request.form['selected_ink_recipe'] 
        print("creating: ", project_name, file_path, process_type, ink_recipe) 

        # Create a process
        with open('../config/processes.json','r') as f:
            process_data = json.load(f)
        
        process_data['processes'][project_name] = {
            'file_path': file_path,
            'process_type': process_type,
            'ink_recipe': ink_recipe, 
            'id': len(process_data['processes']) 
        }

        with open('../config/processes.json','w') as f:
            json.dump(process_data, f)

        return redirect("/list_processes")

    else: 
        process_types = ['extrusion_print', 'cure', 'adhesive_print', 'take_images']
        
        # Get the ink types 
        ink_list = []
        with open('../config/inks.json','r') as f:
            ink_data = json.load(f)
            ink_list = [ink for ink in ink_data]
        
        # Get the print files 
        filenames = os.listdir('../example_artwork')
        
        return render_template("create_process.html", process_types=process_types, ink_list=ink_list, filenames=filenames) 

@app.route('/delete_process/<int:id>') 
def delete_process(id):
    
    with open('../config/processes.json','r') as f:
        process_data = json.load(f)

    print('preparing to delete')
    for process in process_data['processes']:
        if process_data['processes'][process]['id'] == id: 
            print("deleting the process: ", process)
            process_data['processes'].pop(process)
            break

    with open('../config/processes.json','w') as f:
        json.dump(process_data, f)

    return redirect("/list_processes")




@app.route('/start_process/<int:id>')
def start_process(id):
    # 1. Parse the file 
    # 2. Convert to a list of gcodes
    # 3. Load the appropriate tool 
    # 4. Start printing 
    

    # = = = = = = = Load settings = = = = = = = # 
    # Open database 
    with open('../config/processes.json','r') as f:
        process_data = json.load(f) 
    
    # Search database and return process info corresponding to the ID 
    for process in process_data['processes']:
        if process_data['processes'][process]['id'] == id: 
           selected_process = process_data['processes'][process].copy()
    
    # Parse the file 
    file_path = os.path.join(os.path.abspath('../example_artwork'), selected_process['file_path'])
    # polylinesToPrint = readDXF(file_path)
    polylinesToPrint = [ [(0.0,0.0), (10.0, 0.0), (10.0,10.0), (0.0, 0.0)], [(3.0, 3.0), (5.0, 5.0)] ]
    print(file_path) 

    # Load the process settings 
    with open('../config/settings.json','r') as f:
        settings = json.load(f) 
    
    # Load the ink configs
    with open('../config/inks.json','r') as f:
        inks = json.load(f) 

    # Load the ink settings: 
    ink_recipe = selected_process['ink_recipe'] 
    selected_ink_settings = inks[ink_recipe].copy()

    # = = = = = = = Start creating the commands = = = = = = = # 

    machine_code = []

    for polyline in polylinesToPrint:

        machine_code.append('G0 X50 Y50 Z{} F5000'.format(settings['rapid_height']))

        machine_code.append('G0 Z{} F1000'.format(settings['tip_height'])) # Move to a total of 100mm 
        machine_code.append('M106 P0 S1.0')          # Prime (turn the air solenoid on)
        machine_code.append('G4 {}'.format(selected_ink_settings['pause_start']))     # Pause start

        for point in polyline:
            machine_code.append('G0 X{} Y{} F1000'.format(point[0], point[1]))      

        machine_code.append('G4 {}'.format(selected_ink_settings['pause_end']))     # Pause end
        machine_code.append('M106 P0 S0.0') # pressure off
        machine_code.append('G0 Z{}'.format(settings['rapid_height']))     
    print(machine_code)

    # Now we start the print 
    return render_template('home.html') 



if __name__ == "__main__":
    app.run(debug=True) 