#include "DualMC33926MotorShield.h"
// We assume that the two back encoders plugged into the interrupt pins
// Note: interrupt pin 0 is actually pin 2
// Note: interrupt pin 1 is actually pin 3

#define ENCODER_PIN_BACK_LEFT 2
#define ENCODER_PIN_BACK_RIGHT 3
#define ENCODER_PIN_FRONT_LEFT 5
#define ENCODER_PIN_FRONT_RIGHT 6

DualMC33926MotorShield md;
volatile long left_encoder_counter = 0;
volatile long right_encoder_counter = 0;
bool update_PWM = false;
volatile int left_PWM = 0;
volatile int right_PWM = 0;
volatile unsigned long t = 0;
//Mark quadrature packets with DEADBEEF
byte quad_packet[] = {0xDE,0xAD,0xBE,0xEF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
//Mark sonar packets with DEAFFEED
byte sonar_packet[] = {0xDE,0xAF,0xFE,0xED,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};

void setup() {
  // put your setup code here, to run once
  Serial.begin(115200);
  md.init();
  attachInterrupt(0, left_encoder_interrupt_function, CHANGE);
  attachInterrupt(1, right_encoder_interrupt_function, CHANGE);
  t = millis();
}

void loop() {
  //TODO:
  //Handle PING sensor here
  //Get a reading periodically
  ////if that reading tells us there is an object close
  //////disable interupts (noInterrupts();)
  //////while there is an object in front of us
  ////////repeatedly send PWM = 0,0
  //////enable interupts (interrupts();)

  //Handle quadrature
  if(millis() > t + 500){ //wait 500 milliseconds without wasting cycles
    t = millis();
    //capture the current values for transmission (these are volatile!)
    //TODO: mutex lock?
    long _left_encoder_counter = left_encoder_counter;
    long _right_encoder_counter = right_encoder_counter;
    // Serial.print("left ");
    // Serial.print(_left_encoder_counter);
    // Serial.print("right ");
    // Serial.print(_right_encoder_counter);
    // Serial.println();
    //package them up 
    // quad_packet[4] = (byte)(_left_encoder_counter >> 24) & 0xFF;
    // quad_packet[5] = (byte)(_left_encoder_counter >> 16) & 0xFF;
    // quad_packet[6] = (byte)(_left_encoder_counter >> 8) & 0xFF;
    // quad_packet[7] = (byte)(_left_encoder_counter) & 0xFF;
    // quad_packet[8] = (byte)(_right_encoder_counter >> 24) & 0xFF;
    // quad_packet[9] = (byte)(_right_encoder_counter >> 16) & 0xFF;
    // quad_packet[10] = (byte)(_right_encoder_counter >> 8) & 0xFF;
    // quad_packet[11] = (byte)(_right_encoder_counter) & 0xFF;

    //package them up another way
    memcpy(&quad_packet+4,_left_encoder_counter,4);
    memcpy(&quad_packet+8,_right_encoder_counter,4);

    //send each byte over serial
    for(int i = 0; i < 12; i++){
      Serial.print(quad_packet[i],HEX);
    }
    Serial.print('\n');
    //Serial.println(left_encoder_counter);
    //Serial.println(right_encoder_counter);
    //left_encoder_counter = 0;
    //right_encoder_counter = 0;
  }

  //Set the motor speed
  if(update_PWM){
    set_motor_speed(left_PWM, right_PWM);
    update_PWM = false;
  }

}

void left_encoder_interrupt_function() {
  bool back_left = (digitalRead(ENCODER_PIN_BACK_LEFT) == HIGH);
  bool front_left = (digitalRead(ENCODER_PIN_FRONT_LEFT) == HIGH);

  if(!(back_left || front_left) || (back_left && front_left)) {
    // moving forward
    left_encoder_counter += 1;
  }
  else{ //if((!back_left && front_left) || (back_left && !front_left)) {
    // moving backward
    left_encoder_counter += -1;
  }
}

void right_encoder_interrupt_function() {
  bool back_right = (digitalRead(ENCODER_PIN_BACK_RIGHT) == HIGH);
  bool front_right = (digitalRead(ENCODER_PIN_FRONT_RIGHT) == HIGH);

  if(!(back_right || front_right) || (back_right && front_right)) {
    // moving forward
    right_encoder_counter += 1;
  }
  else{ //if((!back_right && front_right) || (back_right && !front_right)) {
    // moving backward
    right_encoder_counter += -1;
  }
}

void serialEvent() {
  noInterrupts();   //Disable interrupts during this routine
  //PWM packet format: [0xDE 0xAD 0xBE 0xEF LL LL LL LL RR RR RR RR] TODO: ADD PAIRITY
  while(Serial.available()){
      //Seek the packet-header: DEADBEEF
      if((byte)Serial.read() != 0xDE)
        continue;
      if((byte)Serial.read() != 0xAD)
        continue;
      if((byte)Serial.read() != 0xBE)
        continue;
      if((byte)Serial.read() != 0xEF)
        continue;

      byte l_buff[4];
      byte r_buff[4];
      Serial.readBytes(l_buff, 4);
      Serial.readBytes(r_buff, 4);

      memcpy(&left_PWM, &l_buff, 4);
      memcpy(&right_PWM, &r_buff, 4);
      update_PWM = true;
   }
   interrupts(); //We are done, re-enable interrupts
}

void stopIfFault()
{
  if (md.getFault())
  {
    Serial.println("fault");
    while (1);
  }
}

// set the motor speed
void set_motor_speed(int left_pwm, int right_pwm) {
  md.setM1Speed(left_pwm);
  md.setM2Speed(right_pwm);
  stopIfFault(); 
  //delay(2);
}
