# circuitprinter
The goal of this project is to print additive circuit traces on the E3D and Jubilee toolchanging 3D printers


# Bill of materials: 
https://docs.google.com/spreadsheets/d/1qsuu0mqhYLWQeWLX05LpEEylz75LFKVL712LdSZb1z4/edit?usp=sharing


# Constraints
* Start with a DXF using named layers for process definition 
* Json database for now, especially when defining and fleshing things out


## Flask app Development setup

### 1. Install dependencies
* pip3 install -r requirements.txt 
* pip3 install mysqlclient
* brew install mysql 
* brew services start mysql 


### 2. Install workbench
- create schema -> circuitprinter

### 3. Initialise Tables
- python refreshdb.py

### 4. Start app
- python app.py

## Setup process

### 1. Startup 
1. Load previous configuration 
2. Home axes 
### 2. Processing 
- Parse file 
- Convert to machine code 
- Run machine code 
### 3. Go
- Select project and go 


# Printing process 
(PRESETS) 
* Select tool 
* Initial extrusion in artwork print 
* For each line: 
    * Rapid to line location in XY at RAPID_HEIGHT 
    * Drop to from RAPID HEIGHT to PRINT_HEIGHT 
    * Prime (START_PRESSURE) 
    * Delay time (START_DELAY_TIME) 
    * Move from start to end with (PRINT_SPEED) 
    * Delay time (END_DELAY_TIME) 
    * Prime (END_PRESSURE) 
    * Raise to (RAPID HEIGHT) 


# Development state 1 
- Create a process step
    - Process name 
    - Print settings recipe 
    - File to print 
    - Registration (manual for now) 
- Run the process
    - Parse the file 
    - Create the machine code 
    - Run the code 


# Development stage 2 
1. Create a project. Page contains: 
    - form: project name 
    - buttons: next, and cancel 
2. Select a process step to add. Page contains: 
    - Card button: Select from process options 
    - Buttons( cancel or next )
3. Select from dropdowns. Page contains: 
    - recipe (for now don't filter types, ie don't give an error when incorrectly selected ) 
    - process file 
    - tool 
    - Buttons( cancel or done )

