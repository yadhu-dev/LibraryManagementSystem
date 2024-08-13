import serial
import pyautogui

########################################################################################################################
#Assigning

baud_rate = 115200
port = 'COM6'
ser= None


#These are the unwanted message comming from Arduino , We have to Avoid this comming in KeyStroke Event...
Unwanted1 = "Reading failed: Timeout in communication."

Unwanted2 = "Reading failed: A MIFARE PICC responded with NAK."





#############################################################################################################################################
####################################### This Function is used to Initialize the Communication with AtMega ###################################
#############################################################################################################################################
def Initialize_Communication():

    global ser

    try:
    
        ser = serial.Serial(port, baud_rate)
        print(f"-------------Your are Succcessfully Connected to ID Card Reader-------------- {port} port in {baud_rate} baud rate......")
        return ser

    except Exception as e:

        print(f"Error Detected---------> {e}")



#############################################################################################################################################
####################################### This Function is used to IRead the data from AtMega #################################################
#############################################################################################################################################   
def Read_Id():
    
    global ser
    

    try:

        while True:                                                     #Used for Continuous Reading...........
            
            if ser.in_waiting > 0:
                
                roll = ser.readline().decode('utf-8').rstrip()

                print(f"Roll No is : {roll}")                           #prints the data 

                if roll != Unwanted1 and Unwanted2:                     #avoiding the Unwanted Strings
                    
                    pyautogui.typewrite(roll)                           #Keystroke to print data
                    pyautogui.press('enter')                            #KeyStroke to Press Enter

    except Exception as e:

        print(f"Error detected ---------> {e}")

    except KeyboardInterrupt:                                           #Using Keyboard Interrupt to stop the program [CTRL +C]

        ser.close()
        print("KeyBoard Interrupted....")
        print("Program closed......")

###############################################################################################################################



if __name__ == '__main__':

    ser = Initialize_Communication()                                   #Calling Initialize_Communication Function for establish the Communication

    if ser:
         Read_Id()                                                     #Calling the Read ID Function for establish the Reading the data from AtMega
