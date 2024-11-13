#include <Arduino.h>
#include <ESP32Servo.h>

Servo servo1;
Servo servo2;
const int buttonPin = 14;
const int ledPin = 15;

void setup() {
  Serial.begin(9600);
  Serial.println("Servo control");
  servo1.attach(12);
  servo2.attach(13);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
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
    
    servo1.write(angle1);
    servo2.write(angle2);
    
    Serial.print("Received angles: ");
    Serial.print(angle1);
    Serial.print(", ");
    Serial.println(angle2);
    
    digitalWrite(ledPin, HIGH); // Turn on LED when command is received
    delay(1000); // Keep LED on for 1 second
    digitalWrite(ledPin, LOW); // Turn off LED
  }

  // Check button state
  if (digitalRead(buttonPin) == LOW) {
    Serial.println("Button pressed");
  }
}