// We assume that the two back encoders plugged into the interrupt pins
// Note: interrupt pin 0 is actually pin 2
// Note: interrupt pin 1 is actually pin 3

#include "DualMC33926MotorShield.h"

#define ENCODER_PIN_BACK_LEFT 2
#define ENCODER_PIN_BACK_RIGHT 3  //analogWrite
#define ENCODER_PIN_FRONT_LEFT 4
#define ENCODER_PIN_FRONT_RIGHT 5  //analogWrite

volatile long left_encoder_counter = 0;
volatile long right_encoder_counter = 0;

int incoming [2];

DualMC33926MotorShield md;

void setup() {
  // put your setup code here, to run once
  Serial.begin(115200);

  attachInterrupt(0, left_encoder_interrupt_function, CHANGE);
  attachInterrupt(1, right_encoder_interrupt_function, CHANGE);
  md.init();
}

void loop() {

  // put your main code here, to run repeatedly
  Serial.print(left_encoder_counter);
  Serial.print(" ");
  Serial.print(right_encoder_counter);
  Serial.println();
  // Serial.println("sent motor command");

  // if there's a bug and the serial buffer gets too big
  while (Serial.available() > 4 * 2) {
  }

  // sent a message to pi to request motor value
  //TODO: add delay to not request values every time
  Serial.println("Motor Values? Pi");
  while (Serial.available()) {
    // int left_motor_speed = Serial.read();
    for (int i = 0; i < 2; i++) {
      incoming[i] = Serial.read();
    }
    int left_motor_speed = incoming[0];
    int right_motor_speed = incoming[1];
    Serial.print("left speed parse: ");
    Serial.print(left_motor_speed);
    Serial.print(" right speed parse: ");
    Serial.print(right_motor_speed);
    Serial.println();
    // Serial.println();
    set_motor_speed(left_motor_speed, right_motor_speed);
  }

  delay(100);
}

void stopIfFault()
{
  if (md.getFault())
  {
    Serial.println("fault");
//    while (1);
  }
}

void set_motor_speed(int left_speed, int right_speed) {
  md.setM1Speed(left_speed);
  md.setM2Speed(right_speed);
  stopIfFault();
  if (abs(left_speed) % 200 == 100)
  {
    Serial.print("M1 current: ");
    Serial.println(md.getM1CurrentMilliamps());
  }
  if (abs(right_speed) % 200 == 100)
  {
    Serial.print("M2 current: ");
    Serial.println(md.getM2CurrentMilliamps());
  }
  delay(2);
}


void left_encoder_interrupt_function() {
  bool back_left = (digitalRead(ENCODER_PIN_BACK_LEFT) == HIGH);
  bool front_left = (digitalRead(ENCODER_PIN_FRONT_LEFT) == HIGH);

  if ((!back_left && !front_left) || (back_left && front_left)) {
    // moving forward
    left_encoder_counter += 1;
  }
  else if ((!back_left && front_left) || (back_left && !front_left)) {
    // moving backward
    left_encoder_counter += -1;
  }
}

void right_encoder_interrupt_function() {
  bool back_right = (digitalRead(ENCODER_PIN_BACK_RIGHT) == HIGH);
  bool front_right = (digitalRead(ENCODER_PIN_FRONT_RIGHT) == HIGH);

  if ((!back_right && !front_right) || (back_right && front_right)) {
    // moving forward
    right_encoder_counter += 1;
  }
  else if ((!back_right && front_right) || (back_right && !front_right)) {
    // moving backward
    right_encoder_counter += -1;
  }
}
