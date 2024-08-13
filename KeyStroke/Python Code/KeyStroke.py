import serial
import pyautogui


baud_rate = 115200
port = 'COM6'
ser= None

Unwanted1 = "Reading failed: Timeout in communication."

Unwanted2 = "Reading failed: A MIFARE PICC responded with NAK."


def Initialize_Communication():

    global ser

    try:
    
        ser = serial.Serial(port, baud_rate)
        print(f"-------------Your are Succcessfully Connected to ID Card Reader-------------- {port} port in {baud_rate} baud rate......")
        return ser

    except Exception as e:

        print(f"Error Detected---------> {e}")

    
def Read_Id():
    
    global ser
    

    try:

        while True:
            
            if ser.in_waiting > 0:
                
                roll = ser.readline().decode('utf-8').rstrip()

                print(f"Roll No is : {roll}")

                if roll != Unwanted1 and Unwanted2:
                    
                    pyautogui.typewrite(roll)
                    pyautogui.press('enter')

    except Exception as e:

        print(f"Error detected ---------> {e}")

    except KeyboardInterrupt:

        ser.close()
        print("KeyBoard Interrupted....")
        print("Program closed......")


if __name__ == '__main__':

    ser = Initialize_Communication()

    if ser:
         Read_Id()
