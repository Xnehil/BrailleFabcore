#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>
#include <AccelStepper.h>


const int stepsPerRevolution = 2048;
const int stepsPerDegree = stepsPerRevolution / 360;
const char* ssid = "redpucp";
const char* password = "C9AA28BA93";

int steps1 = 0;
bool stepperMoving = false;
// Servo servo1;
// Servo servo2;
const int ledPin = 2;

#define IN1 19
#define IN2 18
#define IN3 5
#define IN4 21

#define MotorInterfaceType 8

// Initialize with pin sequence IN1-IN3-IN2-IN4
AccelStepper myStepper = AccelStepper(MotorInterfaceType, IN1, IN3, IN2, IN4);



AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  pinMode(ledPin, OUTPUT);

  // servo1.attach(12);
  // servo2.attach(13);
  myStepper.setSpeed(2000);
  myStepper.setMaxSpeed(1500);
  myStepper.setAcceleration(500);

  server.on("/angulos", HTTP_POST, [](AsyncWebServerRequest *request){
    Serial.println("Received POST request");
    if (request->hasParam("angle1", true) && request->hasParam("angle2", true)) {
      int angle1 = request->getParam("angle1", true)->value().toInt();
      int angle2 = request->getParam("angle2", true)->value().toInt();
      Serial.print("HTTP POST - Angle1: ");
      Serial.println(angle1);
      Serial.print("HTTP POST - Angle2: ");
      Serial.println(angle2);
      // servo1.write(angle1);
      // servo2.write(angle2);
      Serial.print("Moviendo " + String(angle1 * stepsPerDegree) + " pasos");
      int steps1 = angle1 * stepsPerDegree;
      myStepper.moveTo(steps1*2);
      stepperMoving = true;
      digitalWrite(ledPin, HIGH); // Turn on LED when command is received
      delay(1000); // Optional: Keep LED on for 1 second to indicate action
      digitalWrite(ledPin, LOW); // Turn off LED
      request->send(200, "text/plain", "Ángulos actualizados");
    } else {
      Serial.println("HTTP POST - Missing parameters");
      request->send(400, "text/plain", "Petición incorrecta");
    }
  });

  server.begin();
  Serial.println("Server started");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any leading/trailing whitespace
    command.remove(0, 1); // Remove the opening '('
    command.remove(command.length() - 1, 1); // Remove the closing ')'
    
    int commaIndex = command.indexOf(',');
    int angle1 = command.substring(0, commaIndex).toInt();
    int angle2 = command.substring(commaIndex + 1).toInt();
    
    Serial.print("Serial Input - Angle1: ");
    Serial.println(angle1);
    Serial.print("Serial Input - Angle2: ");
    Serial.println(angle2);
    
    // servo1.write(angle1);
    // servo2.write(angle2);
    int steps1 = angle1 * stepsPerDegree;
    myStepper.moveTo(steps1*2);
    stepperMoving = true;
    Serial.print("Se recibieron los ángulos: ");
    Serial.print(angle1);
    Serial.print(", ");
    Serial.println(angle2);
    Serial.println("\n");
      
    digitalWrite(ledPin, HIGH); // Turn on LED when command is received
    delay(1000); // Keep LED on for 1 second
    digitalWrite(ledPin, LOW); // Turn off LED
  }
    if (stepperMoving) {
    if (myStepper.distanceToGo() == 0) {
      stepperMoving = false; // Movimiento completado
      digitalWrite(ledPin, LOW); // Apaga el LED
      Serial.println("Movimiento completado");
    } else {
      myStepper.run();
    }
  }
}

int angleToSteps(int angle) {
  return angle * stepsPerRevolution / 360;
}