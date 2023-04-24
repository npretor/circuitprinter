# bin/bash 
source venv/bin/activate
# Start two scripts co-currently and run in the background 
# need to change sys.path.append('..'), it's running that from here. 
python3 ./src/flask_server/app.py & 
python3 ./src/hardware/MotionServerZMQ.py & 

