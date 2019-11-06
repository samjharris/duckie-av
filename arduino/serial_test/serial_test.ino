#include <avr/wdt.h>

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
char encoderBuffer[5];


void setup() {
  wdt_enable(WDTO_8S);

  // Serial.begin(9600);
  Serial.begin(115200);

  // initialize LED for debugging
  pinMode(13, OUTPUT);
}



void loop() {
  // receive motor commands
  if(Serial.available()) {
    char newChar = Serial.read();

    // read in motor command bytes
    if(motorBufferIndex < 4 || newChar != 'A') {
      motorBuffer[motorBufferIndex] = newChar;
      motorBufferIndex++;
    }
    else {
      // if we have read both motor commands into the motor buffer

      // reset the index back to the start
      motorBufferIndex = 0;

      // drain the rest of the buffer to prevent errors
      while(Serial.available()) { Serial.read(); }

      // unpack the motor commands
      union ShortsOrBytes shortsOrBytes;
      for(char i = 0; i < 4; i++) {
        shortsOrBytes.justBytes[i] = motorBuffer[i];
      }
      short motorLeftTemp = shortsOrBytes.twoShorts.leftMotor;
      short motorRightTemp = shortsOrBytes.twoShorts.rightMotor;

      // TODO: run left motor
      // TODO: run right motor


      // TODO: set these values to the values of the encoder
      signed short left_encoder_counter = 123;
      signed short right_encoder_counter = 456;

      // pack up the encoder values
      char mask = 255;
      encoderBuffer[0] = lowByte(left_encoder_counter);
      encoderBuffer[1] = highByte(left_encoder_counter);
      encoderBuffer[2] = lowByte(right_encoder_counter);
      encoderBuffer[3] = highByte(right_encoder_counter);
      encoderBuffer[4] = 'A';

      // send the encoder values over serial
      Serial.write(encoderBuffer, sizeof(encoderBuffer));
    }

  }

}
