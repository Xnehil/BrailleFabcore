#include <Arduino.h>
#include <Servo.h>
#include <SPIFFS.h>

Servo servo1;  
Servo servo2; 

void setup() {
  Serial.begin(115200);
  SPIFFS.begin(true);  // Initialize SPIFFS

  servo1.attach(9);  
  servo2.attach(10); 
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command == "SEND_FILE") {
      receiveFile();
    } else if (command == "READ_FILE") {
      sendFile();
    } else {
      int angle1 = command.toInt();
      int angle2 = Serial.parseInt();
      servo1.write(angle1);
      servo2.write(angle2);
      Serial.print("Received angles: ");
      Serial.print(angle1);
      Serial.print(", ");
      Serial.println(angle2);
    }
  }
}

void receiveFile() {
  String fileName = Serial.readStringUntil('\n');
  File file = SPIFFS.open(fileName, FILE_WRITE);
  if (!file) {
    Serial.println("No se pudo abrir el archivo para escritura");
    return;
  }

  while (Serial.available() > 0) {
    file.write(Serial.read());
  }
  file.close();
  Serial.println("Archivo recibido");
}

void sendFile() {
  String fileName = Serial.readStringUntil('\n');
  File file = SPIFFS.open(fileName, FILE_READ);
  if (!file) {
    Serial.println("No se pudo abrir el archivo para lectura");
    return;
  }

  while (file.available()) {
    Serial.write(file.read());
  }
  file.close();
  Serial.println("Archivo enviado");
}