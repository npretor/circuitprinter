# Install list 

1. Install <a href="https://github.com/nvidia/jetson-gpio">jetson.gpio </a>
    ```
    pip3 install Jetson.GPIO
    pip3 install 
    sudo groupadd -f -r gpio
    sudo usermod -a -G gpio dlinano
    sudo cp venv/lib/python3.6/site-packages/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```
2. Neopixel libraries 

3. Install docker container 
* Running jetpack 4.6

    ### Getting the camera to work (imx477) 
    ```
    sudo docker run --runtime nvidia -it --rm --network=host -v /tmp/argus_socket:/tmp/argus_socket dustynv/opencv:r32.7.1 
    pip3 install nanocamera 
    python3 
    >>> import nanocamera as nano 
    >>> camera = nano.Camera(width=3840, height=2160)
    >>> frame = camera.read() 
    ```


    ### Getting the gpio accessable in the container 

    ### 
    Running the image server 
    ```
    sudo docker run --runtime nvidia -it --rm --network=host -v /tmp/argus_socket:/tmp/argus_socket -v ~/github/circuitprinter/:/home/circuitprinter/ dustynv/opencv:r32.7.1 
    ```
    
# Startup 
1. Start the motion server 
```
cd src/hardware/
python3 MotionServerZMQ.py
```
2. 