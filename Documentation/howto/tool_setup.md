# Adding tools 

## General overview 

The order of operations in the config file is as follows: 
1. Overall config (motion setup, gcode type, units)
2. Network settings( WiFi, enable networking and HTTP)
3. Drives 
    - Set direction for all 
    - Set drive hardware map, and speeds 
    - Endstops 
    - Z probe config (I'm using a BLTouch)
    - Heater config 
    - Tool definitions (tool_number, name, extruder_drive_map, heater, fan) , offsets, 
    - Fans
    - load config-override.g file 



<a href="https://docs.duet3d.com/Duet3D_hardware/Duet_2_family/DueX2_and_DueX5"> Duex setup pin mappings:  </a>


## Adding a screw paste extruder 
(assumes Duet, Duex5,  Rep-rap firmware 3+ )
1. Add the tool: <a href="https://docs.duet3d.com/User_manual/Reference/Gcodes#m563-define-or-remove-a-tool"> link </a> and choose a slot: I'm choosing the third slot from the right viewed from the back 
2. Set drive direction 
    ```
    M569 P5 S1   # 
    ```
3. Set steps per mm. Motor is 200 steps per rotation. Screw threads move 0.7mm per rotation. Steps per mm is 285.71428. Steps per mm with 16x microstepping is 4571.4285 in position 3
    ```
    M92 X100 Y100 Z1600 C91.022 E834:834:4571.4285:834 
    ```
4. <a href="https://docs.duet3d.com/en/User_manual/Reference/Gcodes#m906-set-motor-currents"> Set motor current. </a> 
>  <i> As a rule of thumb, the recommendation is to set M906 to use 60-85% of the rated maximum current for the motor </i>. 

Rated max is 0.67A/phase @5V. I'll start with 0.67*.75 which is about 0.5A or 500mA. I10 refers to idle current percentage (0-100%)
    ```
    M906 E1000:1000:500:1000 C500 I10
    ```
5. Heater config. Disable heaters for the last two extruders (one will be stepper, one time-pressure ) . Three parameters: 
    * M308 sensor parameters 
    * M950 Set extruder headter 
    * M143 Set temperature limit 
6. Tool definitions. 
* Remove all heater references 
Starting example for the paste extruder: 
```
M563 P2 S"T2" D2 H1 F2 					; Define tool 0
G10 P0 X0 Y0 Z0 						; Reset tool 0 axis offsets
G10 P0 R0 S0 							; Reset initial tool 0 active, standby to 0C
```

Convert to: 
```
M563 P2 S"T2" D2  				; P(Tool #), S"Tool_name", D(rive #), H(eater #), F(an #)
;G10 P0 X0 Y0 Z0 				; Reset tool 0 axis offsets
;G10 P0 R0 S0 					; Reset initial tool 0 active, standby to 0C
```

7. Fan definitions. These aren't really used for any of the extruders, but are useful for controlling curing and lighting for UV and inspection respectively. 
    > <i> <a href="https://docs.duet3d.com/User_manual/Reference/Gcodes#m950-create-heater-fan-spindle-or-gpioservo-pin">M950 </a> is used to create heaters, fans and GPIO ports and to assign pins to them. Each M950 command assigns a pin or pins to a single device. So every M950 command must have exactly one of the H, F, J, P, S, D (for Duet 3 MB6HC only) or E (in RRF 3.5 and later) parameters. </i>

* M950 i left as is, that just maps pins to names 
* M106 turns the fans on, or configures for thermo sensing. T0 uses 1 and 2, T1 uses 3 and 4. I turned  off 5 through 8. 


## Adding a time-pressure extruder 


## Adding a filament extruder 
