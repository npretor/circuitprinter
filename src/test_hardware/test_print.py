import time 
import sys 
sys.path.append('..')
import Printer 



printer = Printer.Printer() 
printer.connect() 
time.sleep(5)
printer.easy_print(tool_number=2, z_override=13.60) 

printer.disconnect() 