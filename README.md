# Circuitprinter
The goal of this project is to print additive circuit traces on the E3D and Jubilee toolchanging 3D printers
![E3D toolchanger with printed UV material](Documentation/media/E3D_lit_up_printing.jpeg) 
![Latest extruder revision](Documentation/media/IMG_5449.jpeg) 



## Bill of materials: 
<a href="https://docs.google.com/spreadsheets/d/1qsuu0mqhYLWQeWLX05LpEEylz75LFKVL712LdSZb1z4/edit?usp=sharing">link to BOM</a>


## Installation
[Install docs](https://github.com/npretor/circuitprinter/tree/main/src#installation)

## Startup 
### Start the motion server 
```
cd src/hardware
sudo python3 MotionClientZMQ.py
```

### Start the Flask server 
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


# Next steps
- Ignore stitching for now 
- Impliment as many features as possible: 
    - Compare design with scan, highlight top 3 issues 
    - Use segment anything 
    - Query the image with mistral? 
    - Find shorts and breaks 
        - Short and break strategy 
    - Create a way to draw on images and correlate with pixels 
        - Define points to watch the width of 