// We assume that the two back encoders plugged into the interrupt pins
// Note: interrupt pin 0 is actually pin 2
// Note: interrupt pin 1 is actually pin 3

#define ENCODER_PIN_BACK_LEFT 2
#define ENCODER_PIN_BACK_RIGHT 3
#define ENCODER_PIN_FRONT_LEFT 5
#define ENCODER_PIN_FRONT_RIGHT 6

volatile long left_encoder_counter = 0;
volatile long right_encoder_counter = 0;


void setup() {
	// put your setup code here, to run once
	Serial.begin(115200);

	attachInterrupt(0, left_encoder_interrupt_function, CHANGE);
	attachInterrupt(1, right_encoder_interrupt_function, CHANGE);
}

void loop() {
	// put your main code here, to run repeatedly
	Serial.print(left_encoder_counter);
	Serial.print(" ");
	Serial.print(right_encoder_counter);
	Serial.println();
	delay(50);
}

void left_encoder_interrupt_function() {
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
