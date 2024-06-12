import mysql.connector
import mysql
from flask import Flask, render_template, jsonify, request
import serial
import time
import threading
import pyautogui

app = Flask(__name__)
stop_event = threading.Event()


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

# Search rfid in the database (iterative function)
cursor = mydb.cursor()

# Function for passing the query
def query_database(uid, cursor):
    cursor.execute("SELECT no FROM details WHERE uid = %s", (uid,))
    return cursor.fetchone()

def search_rfid():
    try:
        while not stop_event.is_set():
            if ser.in_waiting > 0:
                uid = ser.readline().decode('utf-8').strip() # Formatting the UID
                print(f'Received UID : {uid}')
                result = query_database(uid, cursor) # Query function call
                if result:
                    roll_number = str(result[0]) # Assuming UID is the only result in a new line
                    print(f"Roll No: {roll_number}")
                    time.sleep(0.5)

                    pyautogui.typewrite(roll_number)
                    pyautogui.press('enter')
                else:
                    print("UID not found in the database")
    except Exception as e:
        print(f"Error: {e}")

search_thread = threading.Thread(target=search_rfid) # Thread to handle keystrokes in the background

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

#############################################################
######## CLOSE END POINT FOR AUTOMATICALLY FETCHING UID######
#############################################################


############################################################
######## PUSHING THE DATA TO THE DATABASE ##################
############################################################

@app.route('/postdata', methods=['POST'])
def postdata():
    data = request.get_json() # Receive data from the card and the user
    rollno = data.get('rollno', '')
    uid = data.get('uid', '')
    print(f"Received rollno: {rollno}\nReceived UID: {uid}")

    try:
        para = (uid, rollno)
        query = "INSERT INTO details (uid, no) VALUES (%s, %s)" # Query for data insertion

        mycursor.execute(query, para)
        mydb.commit()
        print(f"{mycursor.rowcount} record(s) inserted.")
        return jsonify({'status': 'success', 'received_rollno': rollno, 'received_uid':uid})
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'status': 'failed', 'received_rollno': rollno, 'received_uid':uid})

############################################################
######## CLOSE PUSHING THE DATA TO THE DATABASE ############
############################################################

@app.route('/fetchData')
def fetchData():
    if not search_thread.is_alive():
        stop_event.clear()  # Clear the event in case it was previously set
        search_thread = threading.Thread(target=search_rfid)
        search_thread.daemon = True
        search_thread.start()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'running'})
    
@app.route('/endFetch')
def endFetch():
    if search_thread.is_alive():
        stop_event.set()  # Signal the thread to stop
        search_thread.join()  # Wait for the thread to actually stop
        return jsonify({'status': 'stopped'})
    else:
        return jsonify({'status': 'not running'})

if __name__ == '__main__':
    app.run()