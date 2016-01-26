#ifndef hello_world
#define hello_world

class StringWriter
{
public:
  StringWriter(char *default_string);
  void set_string(char *new_string);
  void write_string();
private:
  char *string_to_write;
};

#endif
