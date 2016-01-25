/**
* This librar
*/
#ifndef temperature_control_h
#define temperature_control_h

namespace temperature_control {
  void initialize_input_pins();
  void initialize_output_pins();
  void create_serial_buffer();
  void read_serial_buffer(); 
}

#endif
