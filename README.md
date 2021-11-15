# circuitprinter
The goal of this project is to print additive multilayer circuits


# Bill of materials: 
https://docs.google.com/spreadsheets/d/1qsuu0mqhYLWQeWLX05LpEEylz75LFKVL712LdSZb1z4/edit?usp=sharing


# Software 
### Libraries used: 
-  https://gpiozero.readthedocs.io/en/stable/api_output.html#digitaloutputdevice

### Duet3D IO control
- Truly at the same time the most exhaustive and the most unreadable documentation I've ever read, especially around which pins map to what
- Let's use fan 7. Should be P27

``` 
Tried: 
M106 P0 S0.0   

M307 P27 I-1  ?disables? a fan
M42 P27 S1.0  - nope, this doesn't work

To try: 
M106 P7 S1.0
    

``` 

This works on Fan0, but not anything on the Duex board. Probably will kill the solenoid eventually

