#include "hello_world.hpp"

int main(){
  char default_string = 'Howdy';
  StringWriter writer = new StringWriter(&default_string);

  writer.write_string();

  char string_to_set = 'Hello World';
  writer.set_string(&string_to_set);
  writer.write_string();
  return 0;
}
