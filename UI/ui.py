import mysql.connector
from flask import Flask, render_template, jsonify
import serial
import time
import threading

app = Flask(__name__)


############################################################
######## START FUNCTION FOR AUTOMATICALLY FETCHING UID######
############################################################
try:
    ser = serial.Serial('COM5', 115200, timeout=1)
except serial.SerialException as e:
    ser = None
    print(f"Failed to connect to serial port: {e}")

# Global variable to store the last read UID
last_uid = None

# DB creds and initialization
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tiger",
  database ="lms"
)
mycursor = mydb.cursor()

def insertdata(uid, rollno):
    try:
        while True:
            # Read RFID
            uid = read_rfid(ser)
            if uid:
                # Once a valid UID is read, prompt for additional input
                no = input("Enter data: ")
                para = (uid, no)

                # SQL query for inserting data into table
                sqlinput = "INSERT INTO details (uid, no) VALUES (%s, %s)"
                try:
                    # Inserting data
                    mycursor.execute(sqlinput, para)
                    mydb.commit()
                    print(f"{mycursor.rowcount} record(s) inserted.")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                # Prompt the user to continue or end the program
                continue_prompt = input("Do you want to scan another card? (y/n): ").strip().lower()
                if continue_prompt == 'n':
                    print("Ending the program.")
                    break
                # Adding a small delay to avoid rapid continuous polling
                time.sleep(1)
    finally:
        # Close cursor and connection
        mycursor.close()
        mydb.close()
        # Close the serial port
        ser.close()

def read_rfid():
    global last_uid
    if ser is None:
        print("Serial port not available.")
        return
    
    flag = {
        "ets Jul 29 2019 12:21:46", "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)", 
        "configsip: 0, SPIWP:0xee", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00", 
        "mode:DIO, clock div:1", "load:0x3fff0030,len:1184", "load:0x40078000,len:13260", 
        "load:0x40080400,len:3028", "entry 0x400805e4"
    }

    while True:
        if ser.in_waiting > 0:
            rfid_tag = ser.readline().strip().decode('utf-8')  # Read and decode the RFID tag
            if any(flag_str in rfid_tag for flag_str in flag):
                continue
            else:
                last_uid = rfid_tag.strip()
                print("\nRead Successfully: " + last_uid)

# Start a background thread to read RFID data if the serial port is available
if ser is not None:
    thread = threading.Thread(target=read_rfid)
    thread.daemon = True
    thread.start()

############################################################
######## END FUNCTION FOR AUTOMATICALLY FETCHING UID########
############################################################

# HOMEPAGE

@app.route('/')
def index():
    return render_template('index.html')

# HOMEPAGE END

#######################################################
######## END POINT FOR AUTOMATICALLY FETCHING UID######
#######################################################

@app.route('/get_uid')
def get_uid():
    global last_uid
    if last_uid:
        return jsonify({'uid': last_uid})
    else:
        return jsonify({'uid': ''})

#
    

#############################################################
######## CLOSE END POINT FOR AUTOMATICALLY FETCHING UID######
#############################################################


############################################################
######## PUSHING THE DATA TO THE DATABASE ##################
############################################################

if __name__ == '__main__':
    app.run()