import mysql.connector
import mysql
from flask import Flask, render_template, jsonify, request
import serial
import time
import threading
import pyautogui

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
            time.sleep(1)
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

############################################################
######## SEARCH AND KEYSTROKE ENTRY FUNCTION ###############
############################################################

cursor = mydb.cursor()

# Function for passing the query
def query_database(uid, cursor):
    cursor.execute("SELECT no FROM details WHERE uid = %s", (uid,))
    return cursor.fetchone()

def keystrokeEntry(uid, counter):
    global last_uid
    try:
        while counter == 1:
        # If data found in serial
            if ser.in_waiting > 0:
                print(f"Received UID: {last_uid}")
                # Calling the query function to get roll numbers with the associated UID
                result = query_database(last_uid, cursor)
                if result:
                    roll_number = str(result[0])  # Ensure the roll number is a string
                    print(f"Roll number: {roll_number}")

                    time.sleep(0.5)

                    # Typing the roll number to the focused textbox
                    pyautogui.typewrite(roll_number)
                    pyautogui.press('enter')
                else:
                    print("UID not found in the database.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close cursor and connection22BCAE34
        cursor.close()
        mydb.close()
        # Close the serial port
        ser.close()

if ser is not None:
    searchThread = threading.Thread(target=keystrokeEntry)
    searchThread.daemon = True
    searchThread.start()

############################################################
######## SEARCH AND KEYSTROKE ENTRY FUNCTION END ###########
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
    data = request.get_json()
    rollno = data.get('rollno', '')
    uid = data.get('uid', '')
    print(f"Received rollno: {rollno}\nReceived UID: {uid}")

    try:
        para = (uid, rollno)
        query = "INSERT INTO details (uid, no) VALUES (%s, %s)"

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

############################################################
######## START SEARCH AND KEYSTROKE FUNCTION ###############
############################################################

@app.route('/keystrokeData', methods=['POST'])
def keystrokeData():
    data = request.get_json()
    uid = data.get('uid', '')
    counter = data.get('ctr', '')

    try:
        while counter == 1:
            # If data found in serial
            if ser.in_waiting > 0:
                uid = ser.readline().decode('utf-8').strip()
                print(f"Received UID: {uid}")
                # Calling the query function to get roll numbers with the associated UID
                result = query_database(uid, cursor)
                if result:
                    roll_number = str(result[0])  # Ensure the roll number is a string
                    print(f"Roll number: {roll_number}")

                    time.sleep(0.5)

                    # Typing the roll number to the focused textbox
                    pyautogui.typewrite(roll_number)
                    pyautogui.press('enter')
                    if counter == 1:
                        keystrokeData()
                    else:
                        return
                else:
                    print("UID not found in the database.") 
                    if counter == 1:
                        keystrokeData()
                    else:
                        return
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'failed'})

############################################################
######## START SEARCH AND KEYSTROKE FUNCTION ###############
############################################################

if __name__ == '__main__':
    app.run()

