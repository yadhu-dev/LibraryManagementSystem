#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define SS_PIN 5
#define RST_PIN 22

MFRC522 rfid(SS_PIN, RST_PIN);

byte authorizedUID[4] = {0x03, 0xB2, 0x5C, 0x1F};

const char *ssid = "ssid";
const char *password = "pass";
const char* serverUrl = "endpoint";

void setup() {
  Serial.begin(115200);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
  Serial.println("IP: ");
  Serial.print(WiFi.localIP());

  SPI.begin();
  // Initialize RFID reader
  rfid.PCD_Init();

  Serial.println("\nTap RFID/NFC Tag on reader");
}

void sendHttpPostRequest(const char* url, byte *uid, byte uidSize) {
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");

  // Create JSON payload
  StaticJsonDocument<200> jsonDoc;
  JsonArray uidArray = jsonDoc.createNestedArray("uid");
  for (byte i = 0; i < uidSize; i++) {
    uidArray.add(uid[i]);
  }

  String payload;
  serializeJson(jsonDoc, payload);

  int httpCode = http.POST(payload);

  if (httpCode > 0) {
    if (httpCode == HTTP_CODE_OK) {
      String response = http.getString();
      Serial.println("HTTP request sent successfully");
      Serial.println(response);
    } else {
      Serial.println("Failed to send HTTP request");
      Serial.println(httpCode);
    }
  } else {
    Serial.println("Failed to connect");
  }

  http.end();
}

void loop() {
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    if (memcmp(rfid.uid.uidByte, authorizedUID, sizeof(authorizedUID)) == 0) {
      Serial.println("Authorized Tag");
    } else {
      Serial.println("Unauthorized Tag with UID:");
      for (byte i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(rfid.uid.uidByte[i], HEX);
      }
      Serial.println();
    }

    sendHttpPostRequest(serverUrl, rfid.uid.uidByte, rfid.uid.size);

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}
