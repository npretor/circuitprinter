import time 
import sys 
sys.path.append('..')



import Printer 
printer = Printer.Printer() 
printer.connect() 

time.sleep(5)

printer.easy_print()

printer.disconnect() 