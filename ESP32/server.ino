#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>

const char* ssid = "JOSELITO1250";
const char* password = "991125484";

Servo servo1;
Servo servo2;
// const int buttonPin = 14;
// const int ledPin = 15;

AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  servo1.attach(5);
  servo2.attach(18);
  // pinMode(buttonPin, INPUT_PULLUP);
  // pinMode(ledPin, OUTPUT);

  server.on("/angulos", HTTP_POST, [](AsyncWebServerRequest *request){
    if (request->hasParam("angle1", true) && request->hasParam("angle2", true)) {
      int angle1 = request->getParam("angle1", true)->value().toInt();
      int angle2 = request->getParam("angle2", true)->value().toInt();
      servo1.write(angle1);
      servo2.write(angle2);
      // digitalWrite(ledPin, HIGH); 
      // delay(1000); 
      // digitalWrite(ledPin, LOW); 
      request->send(200, "text/plain", "Ángulos actualizados");
    } else {
      request->send(400, "text/plain", "Petición incorrecta");
    }
  });

  server.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); 
    command.remove(0, 1); 
    command.remove(command.length() - 1, 1);

    int commaIndex = command.indexOf(',');
    int angle1 = command.substring(0, commaIndex).toInt();
    int angle2 = command.substring(commaIndex + 1).toInt();
    
    servo1.write(angle1);
    servo2.write(angle2);
    
    Serial.print("Se recibieron los ángulos: ");
    Serial.print(angle1);
    Serial.print(", ");
    Serial.println(angle2);
    Serial.println("\n");
  }
}