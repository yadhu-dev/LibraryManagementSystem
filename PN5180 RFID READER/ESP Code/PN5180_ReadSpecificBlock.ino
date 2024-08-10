/*
  PN5180_ReadSpecificBlock.ino
  -----------------------------
  This program reads a specific block (3rd block, index 2) of data from an RFID tag using the PN5180 module.
  It prints the UID, block size, number of blocks, and the data from the specified block to the Serial Monitor.
  
  Author: Yadhul Mohan
          22CSEL33
          BSc Computer Science and Electronics
          Kristu Jayanti College Autonomous Bangalore

  Date: 10/08/2024
*/

//##########################################################################################################################################################################################



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
//#error Please define your pinout here!
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
  Serial.println(F("PN5180 ISO15693 Read Block Example"));

  nfc.begin();                                                             // Initialize PN5180ISO15693
  nfc.reset();                                                             // Reset PN5180ISO15693
  nfc.setupRF();                                                           // Enable RF field

  Serial.println(F("----------------------------------"));
  Serial.println(F("Initialization complete. Ready to read block data."));
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
  Serial.print(F("Block size="));
  Serial.print(blockSize);
  Serial.print(F(", Number of blocks="));
  Serial.println(numBlocks);

  uint8_t readBuffer[blockSize];

  // Read the 3rd block (index 2 because it's zero-indexed)
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

  delay(1000);  // Wait for 1 second before the next loop iteration
}
