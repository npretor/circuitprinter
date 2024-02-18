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
1. Start the motion server. This connects to the motion, and initializes the camera client 
2. Run the test workflow script. Images should be saved to the cache folder 
3. Test sending, images should be received and saved, but that hasn't been written yet 