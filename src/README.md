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






### Camera testing 
1. Start the motion server in the docker container. This connects to the motion, and initializes the camera client. 
    ```
    sudo docker run --runtime nvidia -it --rm --network=host -v /tmp/argus_socket:/tmp/argus_socket -v ~/github/circuitprinter/:/home/circuitprinter/ dustynv/opencv:r32.7.1
    source venv/bin/activate
    pip3 install setuptools packaging pyzmq pyserial imagezmq nanocamera
    cd home/circuitprinter/src/hardware/
    python3 MotionServerZMQ.py 
    ```
2. Run the test workflow script in another script in the container. Images should be saved to the cache folder 
    
    ```
    docker exec -it  b0c3ee90d132 /bin/bash
    source venv/bin/activate 
    cd /home/github/circuitprinter/src
    python3 Workflow.py 
    ```
3. Test sending, images should be received and saved, but that hasn't been written yet. 

