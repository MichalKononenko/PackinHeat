/**
*
*/
#include <Arduino.h>
#define SERIAL_BUFFER_LENGTH 17

// TODO: Move configuration settings to a separate file

const int INPUT_PINS = [1, 2, 3, 4, 5, 6, 7, 8];
const int OUTPUT_PINS = [30, 32, 34, 36, 38, 40, 42];

const int *SERIAL_BUFFER = new int[SERIAL_BUFFER_LENGTH];

/**
* Loops over all the output pins defined in OUTPUT_PINS, and sets them to output
* mode
*
* @param {int[]} pin_list A list of pins to initialize. The function performs
*   a bound check on the list once on calling.
* @param {mode} mode The mode to which each pin should be set
*/
void initialize_pins(int pin_list, bool mode) {
  int list_size = size(pin_list);
  for (int index = 0; index < list_size; i++){
    pinMode(pin_list[index], mode);
  }
}

void initialize_output_pins(int pin_list) {
    return initialize_pins(pin_list, OUTPUT);
}

void initialize_input_pins(int pin_list) {
    return initialize_pins(pin_lit, INPUT);
}

int *create_serial_buffer(int length){
    int *p = new int[length];
    return p
}
    
    
void setup() {
  pinMode(power, OUTPUT);
  initialize_output_pins(OUTPUT_PINS);
  initialize_input_pins(INPUT_PINS);

}

int read_serial_buffer(buffer_address) {

}
