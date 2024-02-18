import time 
import serial 
import re
import serial.tools.list_ports

def get_duet_port():
    ports = serial.tools.list_ports.comports()
    duet_port = None 

    for port, desc, hwid in sorted(ports):
        # print("   {}: {} [{}]".format(port, desc, hwid)) 
        if desc == 'Duet':
            duet_port = port 

    return duet_port 

def get_duet_ip(serial_port):

    if serial_port is None:
        print('ERROR: Invalid port:', serial_port)
        return []
    try:
        ser = serial.Serial(serial_port, 115200, timeout=1)
    except:
        print("ERROR: could not open port: ",serial_port)
        return []
    
    ser.readline()
    success = ser.write(b'M552\n')  
    response = str(ser.readline())
    ser.close()

    # print("Duet response: ",response)

    # Check for a few things 
    # import ipdb; ipdb.set_trace()

    if 'WiFi module is connected' in response: 
        partial_response = response.split(',')[-1] 
        match = re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", partial_response) 
        return match[0]
    else:
        return []


def connect_to_wifi(ssid, password, port='/dev/ttyACM0'):
    """
    
    """
    return False 
    # Connect to serial 
    try:
        ser = serial.Serial(serial_port, 115200, timeout=1)
    except:
        return False

    # Check status 
    status = ser.send(b"M552\n")
    res = str(ser.readline())

    if "module is disabled" in res:
        # Startup 
        send("M552 S0") 

        # Check for startup 
        if "module is started" in res:
            print('wifi started')
            pass
    
    # Stop 
    stop_wifi_command = "M552 S-1"
        
    # Start in idle 
    start_wifi_command = "M552 S0"

    # Get status 
    get_wifi_module_status_command = "M552"



    # Send the wifi credentials 
    send_wifi_credentials = f'M587 S"{str(ssid)}" P"{s(password)}"' 
    
    connect_to_network = "M552 S1"

    if ip_address in res:
        return ip_address 


if __name__ == '__main__':
    serial_port = get_duet_port()
    print("Duet port: ", serial_port)

    res = get_duet_ip(serial_port) 
    print("Duet IP address: ", res)
