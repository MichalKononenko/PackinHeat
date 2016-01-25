#include <Arduino>
#include <CppUnit>
#include "../src/temperature_control.cpp"

class TestInitializePin : public CppUnit::TestCase {
public:
  TestInitializePin( std::string name ) : CppUnit::TestCase( name ){}

  void runTest(){
    const int pins = [1, 2, 3, 4];
    initialize_pins(pins, OUTPUT)
  }
}
