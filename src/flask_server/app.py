"""
Nathan Pretorius 2022
"""

from collections import defaultdict
from flask import Flask, request, render_template, jsonify, redirect
from flask.views import View, MethodView
import sys
sys.path.append('../')

from printer import Printer

import glob, os 
import json
import threading

app = Flask(__name__)

printer = Printer()
surfacePath = []


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/step1_upload", methods={"GET", "POST"}) 
def step1_upload():
    if request.method == "POST":
        design_file_name = request.form['filename'] 
        print(design_file_name) 
        design_path = os.path.join('../example_artwork', design_file_name) 

        surfacePath = printer.parseDesign(design_path)

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
        
        return render_template('step2_show_parsing.html')

@app.route("/step3_config", methods={"GET", "POST"})
def step3_config():
    if request.method == "POST":
        process_recipe_name = request.form['process_recipe'] 
        ink_recipe_name = request.form['selected_ink_recipe'] 
        tool_number = request.form['tool_number'] 

        print("ink recipe: ",ink_recipe_name)
        print('process_type: ', process_recipe_name)
        print('tool number: ', tool_number)

        # TODO: Get process settings to apply to machine code 
        with open('../config/process_recipes.json','r') as f:
            process_recipes = json.load(f) 


        # TODO: Read machine settings for tool offsets


        # TODO: Get ink recipe to pass to 
        # Ink recipes
        with open('../config/inks.json','r') as f:
            ink_data = json.load(f)
        #printer.createMachineCode(surfacePath, tool_number, process_recipes[process_recipe_name], ink_data[ink_recipe_name])

        return redirect('/step4_run')
    else:
        # Get process configs
        #process_types = ['extrusion_print', 'cure', 'adhesive_print', 'take_images']
        process_recipes = []
        with open('../config/process_recipes.json','r') as f:
            process_recipe_data = json.load(f)
            process_recipes = [recipe for recipe in process_recipe_data]    
        
        # Get tools 
        tool_numbers = [1,2,3,4] 

        # Get ink list
        ink_list = []
        with open('../config/inks.json','r') as f:
            ink_data = json.load(f)
            ink_list = [ink for ink in ink_data]         
        return render_template('step3_config.html', process_recipes=process_recipes, tool_numbers=tool_numbers, ink_list=ink_list) 

@app.route("/step4_run", methods={"GET", "POST"}) 
def step4_run():
    if request.method == "POST":
        pass
    else:    
        return render_template('step4_run.html')





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