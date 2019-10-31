#include "DualMC33926MotorShield.h"

DualMC33926MotorShield md;



// We assume that the two back encoders plugged into the interrupt pins
// Note: interrupt pin 0 is actually pin 2
// Note: interrupt pin 1 is actually pin 3

#define ENCODER_PIN_BACK_LEFT 2
#define ENCODER_PIN_BACK_RIGHT 3
#define ENCODER_PIN_FRONT_LEFT 5
#define ENCODER_PIN_FRONT_RIGHT 6

volatile long left_encoder_counter = 0;
volatile long right_encoder_counter = 0;

const int encoder_debounce_time = 10; 

volatile long last_update_left;
volatile long last_update_right;
long encodersLastSent;

void flash(int n) {
  for(int i = 0; i < n; i++) {
    digitalWrite(13,HIGH);
    delay(50);
    digitalWrite(13,LOW);
    delay(20);
  }
}


void stopIfFault() {
  if (md.getFault()) {
    // Serial.println("fault");
    // while(1);
  }
}


void left_encoder_interrupt_function() {
  // debounce the encoder
  if(millis() < last_update_left + encoder_debounce_time) 
    return;
  last_update_left = millis();

  bool back_left = (digitalRead(ENCODER_PIN_BACK_LEFT) == HIGH);
  bool front_left = (digitalRead(ENCODER_PIN_FRONT_LEFT) == HIGH);

  if((!back_left && !front_left) || (back_left && front_left)) {
    // moving forward
    left_encoder_counter += 1;
  }
  else if((!back_left && front_left) || (back_left && !front_left)) {
    // moving backward
    left_encoder_counter += -1;
  }
}

void right_encoder_interrupt_function() {
  // debounce the encoder
  if(millis() < last_update_right + encoder_debounce_time)
    return;
  last_update_right = millis();

  bool back_right = (digitalRead(ENCODER_PIN_BACK_RIGHT) == HIGH);
  bool front_right = (digitalRead(ENCODER_PIN_FRONT_RIGHT) == HIGH);

  if((!back_right && !front_right) || (back_right && front_right)) {
    // moving forward
    right_encoder_counter += 1;
  }
  else if((!back_right && front_right) || (back_right && !front_right)) {
    // moving backward
    right_encoder_counter += -1;
  }
}


void setup() {
  Serial.begin(9600);
  // Serial.begin(115200);

  // initialize LED for debugging
  pinMode(13, OUTPUT);


  // initialize encoders
  attachInterrupt(0, left_encoder_interrupt_function, CHANGE);
  attachInterrupt(1, right_encoder_interrupt_function, CHANGE);
  encodersLastSent = millis();
  last_update_left = millis();
  last_update_right = millis();

  // initialize motors
  md.init();
}


void loop() {
  // send encoder values to pi
  if(millis() > encodersLastSent + 500) {
    encodersLastSent = millis();

    // send encoder values
    Serial.print(left_encoder_counter);
    Serial.print(" ");
    Serial.print(right_encoder_counter);
    Serial.println();
  }

  // receive motor commands
  if(Serial.available() >= 4) {

    int leftMotorValue = Serial.parseInt();
    int rightMotorValue = Serial.parseInt();

    // flash(leftMotorValue);
    md.setM1Speed(leftMotorValue);
    stopIfFault();
    md.setM2Speed(rightMotorValue);
    stopIfFault();
  }



  // TODO: remove this in the final program
  delay(100);
}
