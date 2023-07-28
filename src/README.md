# Installation 

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