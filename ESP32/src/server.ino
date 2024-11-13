#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>

const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

Servo servo1;
Servo servo2;
const int buttonPin = 14;
const int ledPin = 15;

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  servo1.attach(12);
  servo2.attach(13);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);

  server.on("/angulos", HTTP_POST, [](AsyncWebServerRequest *request){
    if (request->hasParam("angle1", true) && request->hasParam("angle2", true)) {
      int angle1 = request->getParam("angle1", true)->value().toInt();
      int angle2 = request->getParam("angle2", true)->value().toInt();
      servo1.write(angle1);
      servo2.write(angle2);
      digitalWrite(ledPin, HIGH); // Turn on LED when command is received
      delay(1000); // Keep LED on for 1 second
      digitalWrite(ledPin, LOW); // Turn off LED
      request->send(200, "text/plain", "Angles set");
    } else {
      request->send(400, "text/plain", "Missing parameters");
    }
  });

  server.begin();
}

void loop() {
  // Check button state
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("Button pressed");
  }
}