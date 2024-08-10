/*
  PN5180_ReadAllBlocks.ino
  --------------------------------
  This program reads all blocks of data from an RFID tag using the PN5180 module.
  It prints the UID, block size, number of blocks, and the data from each block to the Serial Monitor.
  
  Author: Yadhul Mohan
          22CSEL33
          BSc ComputerScience and Electronics
          Kristu Jayanti College Autonomous Bangalore

  Date: 10/ 08/ 2024
*/



#include <PN5180.h>                                                // basic functions to control the PN5180 NFC module.
#include <PN5180ISO15693.h>                                        // support for the ISO15693 protocol



//##############################################################################
//define the pins used for interfacing with the PN5180 module
//##############################################################################

#define PN5180_NSS  10
#define PN5180_BUSY 9
#define PN5180_RST  7


//Create a Object "nfc"
PN5180ISO15693 nfc(PN5180_NSS, PN5180_BUSY, PN5180_RST);




//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       setup starts here.....     //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################
void setup() {
  Serial.begin(115200);
  Serial.println(F("PN5180 ISO15693 Read Entire Block Address Data"));

  nfc.begin();                                                                 //PN5180ISO15693 starts begin( nfc is the object )
  nfc.reset();                                                                 //PN5180ISO15693 reset( nfc is the object )
  nfc.setupRF();                                                               // Enable RF field

  Serial.println(F("Uploaded====>  Date: "__DATE__ " || Time: " __TIME__ ));   // This will provide data and time...........

  Serial.println(F("Initialization complete. Ready to read entire block data."));
}

//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       setup stops here.....     //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################





//###################################################################################################################################################
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////       loop starts here.....     //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//###################################################################################################################################################

void loop() {
  delay(2000);                                                                // Wait for 2 seconds before each read

  Serial.println(F("Reading UID..."));
  uint8_t uid[8];
  ISO15693ErrorCode rc = nfc.getInventory(uid);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getInventory: "));
    Serial.println(nfc.strerror(rc));
    return;
  }

  Serial.print(F("UID="));
  for (int i = 0; i < 8; i++) {
    Serial.print(uid[7 - i], HEX);  // LSB is first
    if (i < 2) Serial.print(":");
  }
  Serial.println();

  Serial.println(F("Getting system info..."));
  uint8_t blockSize, numBlocks;
  rc = nfc.getSystemInfo(uid, &blockSize, &numBlocks);
  if (ISO15693_EC_OK != rc) {
    Serial.print(F("Error in getSystemInfo: "));
    Serial.println(nfc.strerror(rc));
    return;
  }

  Serial.print(F("Block size="));
  Serial.print(blockSize);
  Serial.print(F(", Number of blocks="));
  Serial.println(numBlocks);

  Serial.println(F("Reading data from all blocks..."));
  uint8_t readBuffer[blockSize];
  for (int no = 0; no < numBlocks; no++) {
    rc = nfc.readSingleBlock(uid, no, readBuffer, blockSize);
    if (ISO15693_EC_OK == rc) {
      Serial.print(F("Data from block "));
      Serial.print(no);
      Serial.print(F(": "));
      for (int i = 0; i < blockSize; i++) {
        if (readBuffer[i] < 16) Serial.print("0");
        Serial.print(readBuffer[i], HEX);
        Serial.print(" ");
      }
      Serial.print(" ");
      for (int i = 0; i < blockSize; i++) {
        if (isprint(readBuffer[i])) {
          Serial.print((char)readBuffer[i]);
        } else {
          Serial.print(".");
        }
      }
      Serial.println();
    } else {
      Serial.print(F("Error in readSingleBlock #"));
      Serial.print(no);
      Serial.print(F(": "));
      Serial.println(nfc.strerror(rc));
    }
  }

  delay(5000);  // Wait for 5 seconds before the next loop iteration
}
