### Extrusion 
Extrusion volume seems to be tapering off over time. I don't have a way to fix this yet. 
Maybe after every few given mm, add an extra kick command? Or retract less? Or both?  

### Setting gpio commands is broken 
```
$ gpio -g mode ___whatever____ is broken for pwm setting. Currently using full power for the LEDs 
```

### Need to connect the 



### Todo: 
* Cleanup wiring ratsnest 
* Add the raspberry pi breakout hat 
* Connect the vacuum pump to GPIO control. Need to add 12V power supply as well 
* Create a parameter test print function. Print a test pattern in an array 
* Fix the z probing - it's currently not precise enough, so I'm manually zeroing 
* Make a second extruder 

