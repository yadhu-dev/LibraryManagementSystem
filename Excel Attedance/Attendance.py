import serial
import time 
import pyautogui as py 
from datetime import datetime

# Configuration
port = 'COM6' 
baud_rate = 9600



########################################################################################################
##################### Initialize the serial connection #################################################
########################################################################################################
try:
    ser = serial.Serial(port, baud_rate, timeout=1)  
    print("Connected Successfully....")
except Exception as e:
    print(f"Error detected in Connection ----> {e}")
    ser = None  




########################################################################################################
##################### Sending Data to Atmega ###########################################################
########################################################################################################
def send_to_ATmega328(data):
    """Sends data to the Arduino with a newline character."""
    if ser is not None:
        ser.write(data.encode())
        ser.write(b'\n')  
    else:
        print("Serial port not initialized.")



########################################################################################################
##################### come to begin ###########################################################
########################################################################################################
def come_to_begin():
    
    for i in range(1,5):
        py.press('left')




########################################################################################################
##################### Taking Data from Atmega ##########################################################
########################################################################################################
def read_from_ATmega328():
    """Reads data from Arduino."""
    if ser is not None:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data:
                return data
    return None


########################################################################################################
############################ KeyStroke #################################################################
########################################################################################################
def KeyStroke():
    py.typewrite(current_day)
    py.press('right')
    py.typewrite(current_date)
    py.press('right')
    py.typewrite(current_time)
    py.press('right')
    py.press('right')
    py.typewrite(data)
    py.press('enter')
    come_to_begin()





########################################################################################################
##################### Here Starts ######################################################################
########################################################################################################
if ser:

    time.sleep(0.5)
    
    try:
        while True:
                                                 ##############################################################
            send_to_ATmega328("Read")            # from Here we are sending the commanand to 'Read' Atmega328 #
                                                 ##############################################################
            time.sleep(0.5)
            
           
            data = read_from_ATmega328()           # get the data from ATmega328....
            if data:
                print(f"Data: {data}")             # print the data
                current_day = datetime.now().strftime('%A')
                current_date = datetime.now().strftime('%d-%m-%Y')
                current_time = datetime.now().strftime('%I:%M:%S %p')
                KeyStroke()
                
                
            
            time.sleep(0.3)
                
    except KeyboardInterrupt:                                          
        print("Interrupted by user")
    except Exception as e:
        print(f"Error in Reading: {e}")
    finally:
        ser.close()
        print("Serial connection closed")
else:
    print("Failed to establish serial connection.")
