# Circuitprinter
The goal of this project is to print additive circuit traces on the E3D and Jubilee toolchanging 3D printers



## Bill of materials: 
<a href="https://docs.google.com/spreadsheets/d/1qsuu0mqhYLWQeWLX05LpEEylz75LFKVL712LdSZb1z4/edit?usp=sharing">link to BOM</a>


## Installation

1. Install dependencies
```
brew install mysql 
brew services start mysql 
pip3 install -r requirements.txt

To connect run:
    mysql -u root
```

2. Start virtual environment 
```

```
3. Install workbench
- create schema -> circuitprinter

3. Without workbench
- mysql -u root
- show databases;
- create schema circuitprinter;
- use circuitprinter;
- show tables;
- 
3.1 Initialise Tables
```
python refreshdb.py
```
3.2 Check tables were initialized
```
mysql> show tables;
mysql> describe process;
mysql> select * from process limit 1;
```

5. Start app
```
python app.py
```


# Development stage 1 
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

