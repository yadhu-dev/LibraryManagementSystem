/*
  MFRC522_ReadSpecificBlock.ino
  --------------------------------
  This program reads a specific block of data from an RFID tag using the MFRC522 module.
  It prints the UID and data from the specified block to the Serial Monitor.
  The reading process stops if a `#` character is encountered.

  Author: Yadhul Mohan
          22CSEL33
          BSc Computer Science and Electronics
          Kristu Jayanti College Autonomous Bangalore

  Date: 13/ 08/ 2024
*/

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define buzzer 8

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  Serial.begin(115200);  // Set the baud rate to 115200
  SPI.begin();           // Init SPI bus
  mfrc522.PCD_Init();    // Init MFRC522 card
  pinMode(buzzer, OUTPUT);
  start();
}

void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }


  // Authenticate using key A
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;  // Default key for all sectors

  // Select the 1st sector, 4th block (which is actually block 4, as blocks are 0-indexed)
  byte blockAddr = 4;
  byte buffer[18];
  byte size = sizeof(buffer);


  MFRC522::StatusCode status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockAddr, &key, &(mfrc522.uid));
  
  // Read data from the block
  status = mfrc522.MIFARE_Read(blockAddr, buffer, &size);
  if (status == MFRC522::STATUS_OK) {


    // Convert to ASCII and display on the serial monitor until '#' is encountered
    
    for (byte i = 0; i < 16; i++) {
      if (buffer[i] == '#') {  
        break;
      }
      if (buffer[i] >= 32 && buffer[i] <= 126) {  // Printable ASCII range
        Serial.print((char)buffer[i]);
      } else {
        Serial.print('.');
      }
    }
    Serial.println();
    detectedSound();
  } else {
    if (status == MFRC522::STATUS_MIFARE_NACK) {
    } else {
      Serial.print("Reading failed: ");
      Serial.println(mfrc522.GetStatusCodeName(status));
    }
  }

  // Halt PICC
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}


void start(){


  for(int i =0; i<=4; i++){

    digitalWrite(buzzer,HIGH);
    delay(50);
    digitalWrite(buzzer,LOW);
    delay(50);
  }

}

void detectedSound(){

    digitalWrite(buzzer,HIGH);
    delay(50);
    digitalWrite(buzzer,LOW);

}
