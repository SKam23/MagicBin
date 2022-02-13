// Written by Alex Yoon
// Use for CMU Build18 Hackathon 2022 Magic Bin Project

#include <Servo.h>
#include <Wire.h>
#include <SerLCD.h>

Servo left;
Servo right;
SerLCD lcd;

const int button1 = 2;
const int button2 = 1;
int buttonstate1 = 0;
int buttonstate2 = 0;
int pos = 95;   
String nom = "Arduino";
String msg;

void setup() {
  Wire.begin();
  lcd.begin(Wire);
  left.attach(9); 
  right.attach(10);
  pinMode(button1, INPUT);
  pinMode(button1, INPUT);
  Serial.begin(9600);
}

void readSerialPort() {
  msg = "";
  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      msg += (char)Serial.read();
    }
    Serial.flush();
  }
}
void sendData() {
  //write data
  Serial.print(nom);
  Serial.print(" received : ");
  Serial.print(msg);
  }

void loop() { 
  readSerialPort();
  buttonstate1 = digitalRead(button1);
  buttonstate2 = digitalRead(button2);

  if (Serial.available()) {
    delay(100);
    lcd.clear();
    while (Serial.available()>0) {
      lcd.write(Serial.read());
    }

  }

  else if (msg == "A" || buttonstate1 == HIGH)
  {
    sendData();
    for (pos = 95; pos <= 180; pos += 1) 
    { 
      left.write(pos);              
      right.wri`te(180-pos);
      delay(10);                      
    }
  delay(1500);
    for (pos = 180; pos >= 95; pos -= 1) 
    { 
      left.write(pos);
      right.write(180-pos);          
      delay(10);
    } 
  }
  else if (msg == "B" || buttonstate2 == HIGH)
  {
    sendData();
    for (pos = 95; pos >= 0; pos -= 1) 
    { 
      left.write(pos);
      right.write(180-pos);          
      delay(10);
    }
  delay(1500);
    for (pos = 0; pos <= 95; pos += 1) 
    { 
      left.write(pos);
      right.write(180-pos);          
      delay(10);                         
    }
  }
}
