/*
  PN5180_WriteBlock.ino
  ----------------------
  This program writes data to a specific block (3rd block, index 2) of an RFID tag using the PN5180 module.
  It prompts the user to enter data via the Serial Monitor, writes this data to the specified block,
  and then reads back the data to confirm the write operation.

  Author: Yadhul Mohan
          22CSEL33
          BSc Computer Science and Electronics
          Kristu Jayanti College Autonomous Bangalore

  Date: 10/08/2024
*/


//######################################################################################################################################################################################

#include <PN5180.h>                                                // Basic functions to control the PN5180 NFC module.
#include <PN5180ISO15693.h>                                        // Support for the ISO15693 protocol

//##############################################################################
// Define the pins used for interfacing with the PN5180 module
//##############################################################################

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_MEGA2560) || defined(ARDUINO_AVR_NANO)  // If using Arduino UNO, Arduino MEGA, Arduino NANO

#define PN5180_NSS  10
#define PN5180_BUSY 9
#define PN5180_RST  7

#elif defined(ARDUINO_ARCH_ESP32)    // Else if using ESP32

#define PN5180_NSS  16
#define PN5180_BUSY 5
#define PN5180_RST  17

#else
#error Please define your pinout here!
#endif

// Create an object "nfc"
PN5180ISO15693 nfc(PN5180_NSS, PN5180_BUSY, PN5180_RST);

//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       Setup starts here.....     //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################

void setup() {
  Serial.begin(115200);
  Serial.println(F("=================================="));
  Serial.println(F("PN5180 ISO15693 Write Block Example"));

  nfc.begin();                                                             // Initialize PN5180ISO15693
  nfc.reset();                                                             // Reset PN5180ISO15693
  nfc.setupRF();                                                           // Enable RF field

  Serial.println(F("----------------------------------"));
  Serial.println(F("Initialization complete. Ready to write data to block."));
}

//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       Setup ends here.....       //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################

//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       Loop starts here.....       //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################

void loop() {
  uint8_t uid[8];
  ISO15693ErrorCode rc = nfc.getInventory(uid);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getInventory: "));
    Serial.println(nfc.strerror(rc));
    return;
  }
  
  Serial.print(F("Inventory successful, UID="));
  for (int i = 0; i < 8; i++) {
    Serial.print(uid[7 - i], HEX); // LSB is first
    if (i < 7) Serial.print(":");
  }
  Serial.println();

  uint8_t blockSize, numBlocks;
  rc = nfc.getSystemInfo(uid, &blockSize, &numBlocks);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getSystemInfo: "));
    Serial.println(nfc.strerror(rc));
    return;
  }

  Serial.println(F("----------------------------------"));
  Serial.print(F("Enter data to store in block #3: "));

  // Wait for user input
  while (Serial.available() == 0) {}

  // Read the input data
  String inputData = Serial.readStringUntil('\n');
  inputData.trim();  // Remove any trailing newlines or spaces

  // Convert the input data to hexadecimal format
  uint8_t writeBuffer[blockSize];
  for (int i = 0; i < blockSize; i++) {
    if (i < inputData.length()) {
      writeBuffer[i] = (uint8_t)inputData[i];
    } else {
      writeBuffer[i] = 0x00;  // Pad with zeros if input is shorter than block size
    }
  }

  // Write the data to the 3rd block (block index 2)
  rc = nfc.writeSingleBlock(uid, 2, writeBuffer, blockSize);
  if (ISO15693_EC_OK == rc) {
    Serial.println(F("Data written to block #3 successfully."));
  } else {
    Serial.print(F("Error in writeSingleBlock #3: "));
    Serial.println(nfc.strerror(rc));
  }

  // Read back the data to confirm
  uint8_t readBuffer[blockSize];
  rc = nfc.readSingleBlock(uid, 2, readBuffer, blockSize);
  if (ISO15693_EC_OK == rc) {
    Serial.print(F("Data in block #3: "));
    for (int i = 0; i < blockSize; i++) {
      Serial.print(readBuffer[i], HEX);
      if (i < blockSize - 1) Serial.print(" ");
    }
    Serial.println();
  } else {
    Serial.print(F("Error in readSingleBlock #3: "));
    Serial.println(nfc.strerror(rc));
  }

  delay(5000);  // Delay before next loop iteration
}
