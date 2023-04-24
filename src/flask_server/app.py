"""
Nathan Pretorius 2022
"""

from collections import defaultdict
from flask import Flask, request, render_template, jsonify, redirect
from flask.views import View, MethodView
import sys, time 

sys.path.append('..')
import logging
import glob, os 
import json
import threading
from printer import Printer
# from hardware.MotionController import MotionController
from hardware.MotionClientZMQ import MotionClient

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column, Integer, String, DateTime, Text, Float
# from sqlalchemy.dialects.postgresql import JSONB
# from sqlalchemy_json import mutable_json_type
from database import app, db, Project

# app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

#motion = MotionController(test_mode=False) 
motion = MotionClient() 
# try:
#     motion.connect() 
# except:
#     logging.error('could not connect to motion hardware') 

printer = Printer() 

# move all motion control into printer, for now keep these here 


def silverPrintSetup(toolNumber=1, cal_location=[10, 17, 2]):
    """ Load the tool, move to calibration location """ 
    
    # Load tool
    motion.send("T{}".format(str(toolNumber))) 
    # Set cold extrusion 
    motion.send("M302 P1") 
    # Move to calibration location 
    motion.send("G0 X{} Y{} Z{}".format(cal_location[0], cal_location[1], cal_location[2])) 


@app.route("/", methods={"GET", "POST"}) 
def home():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template('home.html')



# = = = = = = = = Upload        = = = = = = = = # 
# = = = = = = = = Parse         = = = = = = = = # 
# = = = = = = = = Config        = = = = = = = = # 
# Config takes the attributes, and compiles the gcode 
# = = = = = = = = Run           = = = = = = = = # 


# = = = = = = = = Print process = = = = = = = = # 
@app.route("/step1_upload", methods={"GET", "POST"}) 
def step1_upload():
    if request.method == "POST":
        design_file_name = request.form['filename'] 
        print(design_file_name) 

        design_path = os.path.join('../example_artwork', design_file_name) 
        surfacePath = printer.parseDesign(design_path) 
        print(surfacePath)

        return redirect('/step2_show_parsing') 
    else:
        filenames = os.listdir('../example_artwork')
        print(filenames)
        return render_template('step1_upload.html', filenames=filenames)

@app.route("/step2_show_parsing", methods={"GET", "POST"}) 
def step2_show_parsing():
    if request.method == "POST":
        return redirect('/step3_config') 
    else:
        # 1. Get the existing artwork coordinates
        # 2. Convert to coordinates and send to the three.js page 
        # Options: 
        #   https://threejs.org/examples/#webgl_lines_fat
        #   https://github.com/mrdoob/three.js/blob/master/examples/webgl_geometry_shapes.html
        #   https://threejs.org/examples/#webgl_geometry_extrude_shapes
        #   https://threejs.org/examples/#webgl_geometry_extrude_splines
        return render_template('step2_show_parsing.html')

@app.route("/step3_config", methods={"GET", "POST"})
def step3_config():
    """


    """
    if request.method == "POST":
        process_recipe_name     = request.form['process_recipe'] 
        tool_number             = request.form['tool_number'] 
        ink_recipe_name         = request.form['selected_ink_recipe'] 

        print('process_type:  ', process_recipe_name) 
        print('tool number:   ', tool_number) 
        print('ink recipe:    ', ink_recipe_name) 


        # TODO: Get process settings to apply to machine code. Get these from the printer 
        # TODO: Read machine settings for tool offsets
        #cal_location = printer.machine_settings['tools'][str(tool_number)]['tip_zero'] 
        cal_location = printer.machine_settings['tools'][str(1)]['tip_zero'] 
        print("calibration location: ", cal_location) 

        # Load tool and move to calibration location 
        silverPrintSetup(tool_number, cal_location) 
        
        polylines = [
            [(0,0), (10, 0), (10, 10), (0, 10), (0, 0)],
            [(0,0), (9, 0), (9, 9), (0, 9), (0, 0)]
        ]
        
        settings = {
            "rapid_height": 5.0, 
            "rapid_speed": 1000, 
            "print_height": 1.0, 
            "z_calibration": printer.machine_settings['tools'][str(tool_number)]["tip_zero"][2],
            "print_speed": 100.0,
            "start_delay": 0.1,
            "end_delay": .1,
            "gpio": 2, 
        }

        #gcode = printer.createMachineCode(tool_number, process_recipes[process_recipe_name], ink_data[ink_recipe_name])
        printer.machineCode = printer.compilePressureExtrusion(polylines, settings) 

        return redirect('/startPrint') 
    else:
        # Get process configs
        #process_types = ['extrusion_print', 'cure', 'adhesive_print', 'take_images']
        process_recipes = []
        with open('../config/process_recipes.json','r') as f:
            process_recipe_data = json.load(f)
            process_recipes = [recipe for recipe in process_recipe_data]    
        
        # Get tools 
        tool_numbers = [0,1,2,3]  

        # Get ink list
        ink_list = []
        with open('../config/inks.json','r') as f:
            ink_data = json.load(f)
            ink_list = [ink for ink in ink_data]         
        return render_template('step3_config.html', process_recipes=process_recipes, tool_numbers=tool_numbers, ink_list=ink_list) 


@app.route("/saveLocation", methods={"POST"})
def saveLocation():
    if request.method == "POST":
        if "saveLocation" in request.form:
            locations = motion.get_absolute_position() 

            # TODO Get current tool number, and save the current value as the tool z zero 
            printer.machine_settings['tools'][str(request.form[toolNumber])]['tip_zero'] = locations

            logging.info("Saved new tool calibration location: {}".format(printer.machine_settings['tools'][str(request.form[toolNumber])]['tip_zero']))

            if locations == None:
                logging.error("Location parsing error")
            else:
                logging.info("Saving XYZ: {} {} {}".format(locations[0], locations[1], locations[2])) 
        else:
            logging.error("Error, unknown motion request") 
    else:
        logging.error("Posts not supported to this route") 

    return render_template("printCalibration.html") 
 
@app.route("/printCalibration", methods={"GET", "POST"})
def printCalibration():
    if request.method == "POST":
        print(request.form) 
        
        if "x_value" in request.form:
            x = request.form["x_value"] 
            logging.info("Moving x axis: {}".format(x)) 
            motion.gcode('G91') 
            motion.gcode('G0 X{} Y0 Z0'.format(x))   
            motion.gcode('G90') 

        elif "y_value" in request.form:
            y = request.form["y_value"] 
            logging.info("Moving y axis: {}".format(y)) 
            motion.gcode('G91') 
            motion.gcode('G0 X0 Y{} Z0'.format(y))   
            motion.gcode('G90') 

        elif "z_value" in request.form:
            z = request.form["z_value"] 
            logging.info("Moving z axis: {}".format(z)) 
            motion.gcode('G91') 
            motion.gcode('G0 X0 Y0 Z{}'.format(z))   
            motion.gcode('G90') 

        elif "saveLocation" in request.form:
            locations = motion.position() 

            if locations == None:
                logging.error("Location parsing error")
            else:
                logging.info("Saving XYZ: {} {} {}".format(locations[0], locations[1], locations[2]))             

            # TODO Get current tool number, and save the current value as the tool z zero 
            printer.machine_settings['tools'][str(request.form["toolNumber"])]['tip_zero'] = locations
            zip_zero_location = printer.machine_settings['tools'][str(request.form["toolNumber"])]['tip_zero']
            logging.info("Saved new tool calibration location: {}".format( zip_zero_location ))



        elif "getTool" in request.form:
            logging.info("Getting tool {}".format(request.form["toolNumber"]))
            motion.gcode("T{}".format(request.form["toolNumber"])) 
            printer.currentToolNum = int(request.form["toolNumber"])

        elif "replaceTool" in request.form:
            logging.info("Replacing current tool")
            motion.gcode("T-1") 
            printer.currentToolNum = None

        elif "gpio_on" in request.form:
            logging.info("GPIO {} on".format(request.form['gpio_on']))    
            motion.gcode("M106 P{} S1.0".format(request.form['gpio_on']))  

        elif "gpio_off" in request.form:
            logging.info("GPIO {} off".format(request.form['gpio_off']))   
            motion.gcode("M106 P{} S0.0".format(request.form['gpio_off']))  

        else:
            logging.error("Error, unknown motion request")
        
        return render_template("printCalibration.html")            

    else:
        return render_template("printCalibration.html")

@app.route("/startPrint", methods={"GET", "POST"}) 
def startPrint():
    if request.method == "POST":



        return render_template('startPrint.html')
    else:    
        # Assumes the tool is loaded 
        # Assumes the print method is pressure, we can select later 

        logging.info("Starting print")
        logging.info("Printing {} lines of code now".format(len(printer.machineCode)))  
        for line in printer.machineCode:
            motion.gcode(line)         
        return render_template('startPrint.html')


# = = = = = = = = Projects CRUD = = = = = = = = # 
@app.route("/projects", methods=["GET", "POST"])
def projects():
    # = = = = = = = Create = = = = = = = #
    if request.method == "POST":
        content = request.form['content']
        settings = request.form['settings']
        new_project = Project(content=content, settings=json.loads(settings))

        try: 
            db.session.add(new_project) 
            db.session.commit() 
            return redirect('/projects') 
        except:
            return 'There was an error while adding the project' 
    else:
        # = = = = = = = Read = = = = = = = #
        all_projects = Project.query.all()
        return render_template("projects.html", projects=all_projects)

@app.route('/delete/<int:project_id>')
def delete(project_id):
    # = = = = = = = Delete = = = = = = = #
    project_to_delete = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/projects')
    except:
        return 'There was an error while deleting that project'

@app.route('/update/<int:project_id>', methods={'GET', 'POST'})
def update(project_id):
    # = = = = = = = Update = = = = = = = #
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.content = request.form['content']
        project.settings = json.loads(request.form['settings'] or {})

        try:
            db.session.commit()
            return redirect('/projects')
        except:
            return 'There was an issue while updating that project'

    else:
        return render_template('update.html', project=project)

@app.route("/startup_system", methods={"GET", "POST"}) 
def startup_system():
    """
    Homes motion system
    """
    if request.method == "POST": 
        return redirect('/') 
    else:    
        # Home the system
        if motion.connect():
            # Check if the system has been homed

            logging.info("Homing motion system")
            #motion.gcode('G28') 
            logging.info("System ready")
        else:
            logging.error("Could not connect") 

        return redirect('/') 

@app.route('/serve_artwork')
def serve_artwork():
    simple_box = [(0,0), (10,0), (10,10), (0, 10), (0,0)] 
    return jsonify({'simple_box': simple_box}) 

@app.route("/show_artwork", methods={"GET", "POST"})
def show_artwork():
    #simple_box = [(0,0), (500,0), (500,500), (0, 500), (0,0)] 
    simple_box = [[0,0], [500, 0], [500,500], [0,500], [0,0]]


    if request.method == "POST":
        return render_template("show_artwork.html", simple_box=simple_box)
    else:    
        return render_template("show_artwork.html", simple_box=simple_box)

@app.route("/settings", methods={"GET", "POST"}) 
def settings():
    if request.method == "POST":
        pass
    else:
        return render_template('settings.html') 


if __name__ == "__main__":
    app.run(debug=False) 