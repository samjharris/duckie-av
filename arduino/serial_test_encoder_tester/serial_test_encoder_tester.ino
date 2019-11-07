#include <avr/wdt.h>

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
  Serial.print("left encoder count = ");
  Serial.println(left_encoder_counter);
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
  Serial.print("right encoder count = ");
  Serial.println(right_encoder_counter);
}


void setup() {
  // Serial.begin(9600);
  Serial.begin(115200);

  // initialize encoders
  attachInterrupt(0, left_encoder_interrupt_function, CHANGE);
  attachInterrupt(1, right_encoder_interrupt_function, CHANGE);
}


void loop() { }
