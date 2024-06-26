import mysql.connector
import serial
import time

def read_rfid(ser):
    flag = {"ets Jul 29 2019 12:21:46", "rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)", 
            "configsip: 0, SPIWP:0xee", "clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00", 
            "mode:DIO, clock div:1", "load:0x3fff0030,len:1184", "load:0x40078000,len:13260", 
            "load:0x40080400,len:3028", "entry 0x400805e4"}

    while True:
        print("Place your RFID tag near the reader...")
        if ser.in_waiting > 0:
            rfid_tag = ser.readline().strip().decode('utf-8')  # Read and decode the RFID tag
            if any(flag_str in rfid_tag for flag_str in flag):
                continue
            else:
                print("\nRead Successfully")
                return rfid_tag.strip()
       



# Open the serial port
ser = serial.Serial('COM5', 115200, timeout=1)


#Connecting to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="tiger",
  database ="lms"
)
mycursor = mydb.cursor()

#taking values 
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
