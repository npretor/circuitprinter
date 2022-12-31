### Todo
* Python sqlite database for tools and tool settings, calibration settings, basically all defaults in machine settings right now

### Outline of pages to design 

1. Upload a dxf file
    a. Form: upload
    b. Set as current_design_file. 
2. TODO: show the file, empty for now
    a. Buttons: Previous, next. If previous, current_design_file is wiped
    b. D3 visualization of circuit traces on the plater 
3. Select ink settings and process settings
    a. Form: ink_settings dropdown, process_settings dropdown 
    b. Button: previous, start print
4. Start the print 
    a. Show process status updating. Buttons(later): pause, play, stop
