#include ".\hello_world.hpp"
#include <iostream>

StringWriter::StringWriter(char *default_string){
  *string_to_write = *default_string;
}

void StringWriter::set_string(char *new_string){
  *string_to_write = *new_string;
}

void StringWriter::write_string(){
  std::cout << string_to_write << std::endl;
}
