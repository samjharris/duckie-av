#include <avr/wdt.h>

// used for running motors
#include "DualMC33926MotorShield.h"
DualMC33926MotorShield md;

#define PING_PIN 11 //USDS signal pin (one of the few digital GPIOs not used by MC3392)
#define DISTANCE_THRESHOLD 20 //Object detection threshold within which to halt (in cms)

// We assume that the two back encoders plugged into the interrupt pins
// Note: interrupt pin 0 is actually pin 2
// Note: interrupt pin 1 is actually pin 3
#define ENCODER_PIN_BACK_LEFT 2
#define ENCODER_PIN_BACK_RIGHT 3
#define ENCODER_PIN_FRONT_LEFT 5
#define ENCODER_PIN_FRONT_RIGHT 6
volatile short left_encoder_counter = 0;
volatile short right_encoder_counter = 0;

// debouncing the encoders
const int encoder_debounce_time = 10;
volatile long last_update_left;
volatile long last_update_right;

//PING sensor variables
volatile long ping_duration = 0;
volatile long ping_distance = 0;
bool halting = false;
int count = 0;

// used for serial communication
union ShortsOrBytes
{
  struct TwoShorts {
    short leftMotor;
    short rightMotor;
  } twoShorts;
  char justBytes[4];
};
char motorBufferIndex = 0;
char motorBuffer[4];
char encoderBuffer[8];


// called when either of the motors fails
void stopIfFault() {
  if (md.getFault()) {
    // Serial.println("fault");
  }
}


// called when there is a change on the left encoder signal
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

// called when there is a change on the right encoder signal
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
  // wdt_enable(WDTO_8S);
  wdt_disable();

  // Serial.begin(9600);
  Serial.begin(115200);

  // initialize motors
  md.init();

  // initialize encoders
  attachInterrupt(0, left_encoder_interrupt_function, CHANGE);
  attachInterrupt(1, right_encoder_interrupt_function, CHANGE);
  last_update_left = millis();
  last_update_right = millis();
}

//send out a PING chirp
void chirp(){
  pinMode(PING_PIN, OUTPUT);
  digitalWrite(PING_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(PING_PIN, HIGH);
  delayMicroseconds(5);
  digitalWrite(PING_PIN, LOW);
}

void loop() {
  //detect objects
  if(count % 10 == 0) { // check every 1/10 of time
    chirp();
    pinMode(PING_PIN, INPUT);
    ping_duration = pulseIn(PING_PIN, HIGH);
    ping_distance = ping_duration / 29 / 2;
    if(ping_distance <= DISTANCE_THRESHOLD){
      halting = true;
    }else if(halting && ping_distance > DISTANCE_THRESHOLD){
      halting = false;
    }

  }

  count++;

  if(halting){
    md.setM1Speed(0);
    md.setM2Speed(0);
  }
  
  // receive motor commands
  if(Serial.available() && !halting) {
    char newChar = Serial.read();

    // read in motor command bytes
    if(motorBufferIndex < 4 || newChar != 'A') {
      motorBuffer[motorBufferIndex] = newChar;
      motorBufferIndex++;
    }
    // if we have read all the motor command bytes (into the motor buffer)
    else {
      // reset the index back to the start
      motorBufferIndex = 0;

      // drain the rest of the buffer to prevent errors
      while(Serial.available()) { Serial.read(); }

      // unpack the motor commands
      union ShortsOrBytes shortsOrBytes;
      for(char i = 0; i < 4; i++) {
        shortsOrBytes.justBytes[i] = motorBuffer[i];
      }
      short motorLeft = shortsOrBytes.twoShorts.leftMotor;
      short motorRight = shortsOrBytes.twoShorts.rightMotor;

      // run the motors
      md.setM1Speed(motorLeft);
      stopIfFault();
      md.setM2Speed(motorRight);
      stopIfFault();

      // capture volatile values
      short temp_left_encoder_counter = left_encoder_counter;
      short temp_right_encoder_counter = right_encoder_counter;
       
      // pack up the current encoder values
      encoderBuffer[0] = 0xDE;
      encoderBuffer[1] = 0xAD;
      encoderBuffer[2] = lowByte(temp_left_encoder_counter);
      encoderBuffer[3] = highByte(temp_left_encoder_counter);
      encoderBuffer[4] = lowByte(temp_right_encoder_counter);
      encoderBuffer[5] = highByte(temp_right_encoder_counter);
      encoderBuffer[6] = 0xCA;
      encoderBuffer[7] = 0xFE;
      
      // send the encoder values over serial
      Serial.write(encoderBuffer, sizeof(encoderBuffer));
    }
  }
}
