# Circuitprinter
The goal of this project is to print additive circuit traces on the E3D and Jubilee toolchanging 3D printers



## Bill of materials: 
<a href="https://docs.google.com/spreadsheets/d/1qsuu0mqhYLWQeWLX05LpEEylz75LFKVL712LdSZb1z4/edit?usp=sharing">link to BOM</a>


## Installation

### Install python dependencies 
1. Install dependencies
Setup a virtual environment and install python reqs 
```
python3 -m venv venv 
source venv/bin/activate 
python3 -m pip install -r requirements.txt
```
2. Install threejs 
```
cd circuitprinter/src/flask_server/static/repos
git clone https://github.com/mrdoob/three.js.git
```


Mac: 
```
brew install mysql
brew services start mysql 
python3 -m venv venv 
source venv/bin/activate 
pip3 install -r requirements.txt
```

Linux
* Need to install rust for the mysql client 
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh  
sudo apt install mariadb-server default-libmysqlclient-dev python3-dev default-libmysqlclient-dev build-essential
# Install geos 
apt-get install libgeos++
python3 -m venv venv 
source venv/bin/activate 
pip3 install -r requirements.txt 
```

2. Create schema 
```
mysql -u root or sudo mysql -u root -p 
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('');
UPDATE mysql.user SET plugin = '' WHERE user = 'root' AND host = 'localhost';
FLUSH PRIVILEGES;

show databases; 
create schema circuitprinter; 
use circuitprinter; 
show tables; 
```

3. Initialise Tables
```
cd src/flask_server
python refreshdb.py
```
4. Check tables were initialized
```
mysql> show tables;
mysql> describe process;
mysql> select * from process limit 1; 
```

5. Start app
```
python3 app.py
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

