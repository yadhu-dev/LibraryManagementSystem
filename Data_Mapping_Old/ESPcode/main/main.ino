#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define SS_PIN 5
#define RST_PIN 22

#define LED 33
#define STATUS 2

MFRC522 rfid(SS_PIN, RST_PIN);

char card[22];

const char *ssid = "todo";
const char *password = "todotodo";

void setup()
{
  Serial.begin(115200);

  pinMode(LED,OUTPUT);
  pinMode(STATUS, OUTPUT);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }
  digitalWrite(STATUS, HIGH);
  Serial.println("Connected to WiFi");
  Serial.println("IP: ");
  Serial.print(WiFi.localIP());
  Serial.println("");

  SPI.begin();
  // Initialize RFID reader
  rfid.PCD_Init();

  Serial.println("\nTap RFID/NFC Tag on reader");
}

void sendHttpRequest(const char *url, const char *uid, const char *rollno)
{
  if (WiFi.status() == WL_CONNECTED)
  {
    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> jsonDoc;
    jsonDoc["uid"] = uid;
    jsonDoc["rollno"] = rollno;

    String requestBody;
    serializeJson(jsonDoc, requestBody);

    int httpCode = http.POST(requestBody);

    if (httpCode == HTTP_CODE_OK)
    {
      digitalWrite(LED, HIGH);
      delay(10);
      Serial.println("HTTP request sent successfully");
      digitalWrite(LED, LOW);
    }
    else
    {
      Serial.println("Failed to send HTTP request");
      Serial.println(httpCode);
    }

    http.end();
  }
  else
  {
    Serial.println("WiFi not connected");
  }
}

String ConvertToRollno()
{
  MFRC522::MIFARE_Key key;
  for (byte i = 0; i < 6; i++)
  {
    key.keyByte[i] = 0xFF; // Using default key value
  }

  byte sector = 1;
  byte blockAddr = 4;
  byte buffer[18];
  byte bufferSize = sizeof(buffer);

  // Authenticate using key A
  MFRC522::StatusCode status = rfid.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockAddr, &key, &(rfid.uid));

  // Read data from the block
  status = rfid.MIFARE_Read(blockAddr, buffer, &bufferSize);
  if (status == MFRC522::STATUS_OK)
  {
    String rollNo = "";
    for (uint8_t i = 0; i < 16; i++)
    {
      if (buffer[i] >= 32 && buffer[i] <= 126 && buffer[i] != '#')
      {
        rollNo += (char)buffer[i];
      }
    }
    return rollNo;
  }
  else
  {
    return "";
  }
}

void loop()
{
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial())
  {

    // Clear the card array
    memset(card, 0, sizeof(card));

    // Process the UID
    for (byte i = 0; i < rfid.uid.size; i++)
    {
      // Convert each byte to hex and store in the card array
      sprintf(&card[i * 3], "%02X ", rfid.uid.uidByte[i]);
    }

    card[rfid.uid.size * 3 - 1] = '\0';

    // Print the card array for verification
    Serial.print("Card UID: ");
    Serial.println(card);
    String rollNo = ConvertToRollno();
    Serial.print("RollNo: ");
    Serial.println(rollNo);
    Serial.println("");

    // Send the rollno and uid to the server
    sendHttpRequest("http://192.168.5.99:3000/api/endpoint", card, rollNo.c_str());

    // Halt PICC and stop encryption on PCD
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}
