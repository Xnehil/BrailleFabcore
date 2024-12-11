#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>

const char* ssid = "LAPTOP-05R42Q57 3226";
const char* password = "28*7U3f1";

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

AsyncWebServer server(80);

void connectToWiFi() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  int attempts = 0;
  const int maxAttempts = 15;

  while (WiFi.status() != WL_CONNECTED && attempts < maxAttempts) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("Connected to WiFi");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("Failed to connect to WiFi");
  }
}

void initializeServos() {
  servo1.attach(13);
  servo2.attach(12);
  servo3.attach(14);
  servo4.attach(27);
}

void handleServoAngles(int angle1, int angle2, int angle3, int angle4) {
  servo1.write(angle1);
  servo2.write(angle2);
  servo3.write(angle3);
  servo4.write(angle4);
}

// LED Pin for status indication
const int ledPin = 2;

// Struct to hold a pair of angles
struct AnglePair {
  int angleA;
  int angleB;
};

// Define maximum number of angle pairs in the buffer
#define MAX_ANGLE_PAIRS 20

AnglePair angleBuffer[MAX_ANGLE_PAIRS];
int bufferHead = 0;
int bufferTail = 0;

bool isProcessing = false;
bool sendToGroup1 = true;

unsigned long lastUpdateGroup1 = 0;
unsigned long lastUpdateGroup2 = 0;
const unsigned long groupDelay = 2000; 


bool enqueueAnglePair(int a, int b);
bool dequeueAnglePair(AnglePair &pair);
void processBuffer();

void setup() {
  connectToWiFi();
  initializeServos();

  server.on("/angulos", HTTP_POST, [](AsyncWebServerRequest *request){
    if (request->hasParam("angle1", true) && request->hasParam("angle2", true) &&
        request->hasParam("angle3", true) && request->hasParam("angle4", true)) {
      int angle1 = request->getParam("angle1", true)->value().toInt();
      int angle2 = request->getParam("angle2", true)->value().toInt();
      int angle3 = request->getParam("angle3", true)->value().toInt();
      int angle4 = request->getParam("angle4", true)->value().toInt();
      handleServoAngles(angle1, angle2, angle3, angle4);
      request->send(200, "text/plain", "Ángulos actualizados");
    } else {
      request->send(400, "text/plain", "Petición incorrecta");
    }
  });

  server.on("/paqueteAngulos", HTTP_POST, [](AsyncWebServerRequest *request){
    if (request->hasParam("angulos", true)) {
      String angulos = request->getParam("angulos", true)->value();
      // Expected format: [(angle1, angle2), (angle3, angle4), ...]
      
      // Remove surrounding brackets if present
      angulos.trim();
      if (angulos.startsWith("[") && angulos.endsWith("]")) {
        angulos.remove(0, 1);
        angulos.remove(angulos.length() - 1, 1);
      }
      
      // Split the string into individual angle sets
      int start = 0;
      while (angulos.indexOf('(', start) != -1 && angulos.indexOf(')', start) != -1) {
        int openParenthesisIndex = angulos.indexOf('(', start);
        int closeParenthesisIndex = angulos.indexOf(')', openParenthesisIndex);
        if (openParenthesisIndex == -1 || closeParenthesisIndex == -1) {
          break; // Invalid format
        }
        
        String angleSet = angulos.substring(openParenthesisIndex + 1, closeParenthesisIndex);
        start = closeParenthesisIndex + 1;
        
        // Split angles by comma
        int firstComma = angleSet.indexOf(',');
        if (firstComma == -1) {
          Serial.println("Invalid angle set format");
          continue; // Skip invalid angle set
        }
        
        String angleStrA = angleSet.substring(0, firstComma);
        String angleStrB = angleSet.substring(firstComma + 1);
        
        angleStrA.trim();
        int angleA = angleStrA.toInt();
        angleStrB.trim();
        int angleB = angleStrB.toInt();
        
        if (!enqueueAnglePair(angleA, angleB)) {
          Serial.println("Angle buffer full. Some angles were not enqueued.");
          break; // Buffer is full
        }
        
        Serial.print("Enqueued Angle Pair: ");
        Serial.print(angleA);
        Serial.print(", ");
        Serial.println(angleB);
      }
      
      request->send(200, "text/plain", "Ángulos en cola para actualización");
    } else {
      request->send(400, "text/plain", "Petición incorrecta");
    }
  });

  server.begin();
}

void loop() {
  processBuffer();

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.remove(0, 1);
    command.remove(command.length() - 1, 1);

    int commaIndex1 = command.indexOf(',');
    int commaIndex2 = command.indexOf(',', commaIndex1 + 1);
    int commaIndex3 = command.indexOf(',', commaIndex2 + 1);

    int angle1 = command.substring(0, commaIndex1).toInt();
    int angle2 = command.substring(commaIndex1 + 1, commaIndex2).toInt();
    int angle3 = command.substring(commaIndex2 + 1, commaIndex3).toInt();
    int angle4 = command.substring(commaIndex3 + 1).toInt();

    handleServoAngles(angle1, angle2, angle3, angle4);

    Serial.print("Se recibieron los ángulos: ");
    Serial.print(angle1);
    Serial.print(", ");
    Serial.print(angle2);
    Serial.print(", ");
    Serial.print(angle3);
    Serial.print(", ");
    Serial.println(angle4);
    Serial.println("\n");
  }
}

bool enqueueAnglePair(int a, int b) {
  int nextHead = (bufferHead + 1) % MAX_ANGLE_PAIRS;
  if (nextHead == bufferTail) {
    // Buffer is full
    return false;
  }
  
  angleBuffer[bufferHead].angleA = a;
  angleBuffer[bufferHead].angleB = b;
  bufferHead = nextHead;
  return true;
}

// Function to dequeue an angle pair
bool dequeueAnglePair(AnglePair &pair) {
  if (bufferHead == bufferTail) {
    // Buffer is empty
    return false;
  }
  
  pair = angleBuffer[bufferTail];
  bufferTail = (bufferTail + 1) % MAX_ANGLE_PAIRS;
  return true;
}

// Function to process the angle buffer
void processBuffer() {
  if (!isProcessing) {
    AnglePair currentPair;
    if (dequeueAnglePair(currentPair)) {
      unsigned long currentMillis = millis();
      isProcessing = true;
      
      if (sendToGroup1) {
        // Check if enough time has passed since the last update to Group1
        if (currentMillis - lastUpdateGroup1 >= groupDelay) {
          // Send to Servo 1 and Servo 2
          if (currentPair.angleA >= 0 && currentPair.angleA <= 180 &&
              currentPair.angleB >= 0 && currentPair.angleB <= 180) {
            servo1.write(currentPair.angleA);
            servo2.write(currentPair.angleB);
            Serial.print("Updated Servo1 to ");
            Serial.print(currentPair.angleA);
            Serial.print("°, Servo2 to ");
            Serial.print(currentPair.angleB);
            Serial.println("°");
            
            digitalWrite(ledPin, HIGH); // Indicate activity
            // Implement a non-blocking LED off after a short duration
            delay(100); // Brief delay to ensure servo commands are sent
            digitalWrite(ledPin, LOW);
            
            lastUpdateGroup1 = currentMillis; // Update the last sent time
            sendToGroup1 = false; // Switch to the next group
          } else {
            Serial.println("Ángulos fuera de rango en el buffer.");
          }
        } else {
          // Not enough time has passed, re-enqueue the pair at the end
          enqueueAnglePair(currentPair.angleA, currentPair.angleB);
          Serial.println("Esperando para enviar al Grupo1...");
        }
      } else {
        // Check if enough time has passed since the last update to Group2
        if (currentMillis - lastUpdateGroup2 >= groupDelay) {
          // Send to Servo 3 and Servo 4
          if (currentPair.angleA >= 0 && currentPair.angleA <= 180 &&
              currentPair.angleB >= 0 && currentPair.angleB <= 180) {
            servo3.write(currentPair.angleA);
            servo4.write(currentPair.angleB);
            Serial.print("Updated Servo3 to ");
            Serial.print(currentPair.angleA);
            Serial.print("°, Servo4 to ");
            Serial.print(currentPair.angleB);
            Serial.println("°");
            
            digitalWrite(ledPin, HIGH); // Indicate activity
            // Implement a non-blocking LED off after a short duration
            delay(100); // Brief delay to ensure servo commands are sent
            digitalWrite(ledPin, LOW);
            
            lastUpdateGroup2 = currentMillis; // Update the last sent time
            sendToGroup1 = true; // Switch to the next group
          } else {
            Serial.println("Ángulos fuera de rango en el buffer.");
          }
        } else {
          // Not enough time has passed, re-enqueue the pair at the end
          enqueueAnglePair(currentPair.angleA, currentPair.angleB);
          Serial.println("Esperando para enviar al Grupo2...");
        }
      }
      
      isProcessing = false;
    }
  }
}