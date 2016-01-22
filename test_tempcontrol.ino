#include <ArduinoUnit.h>
#include "./tempcontrol.ino"

TestSuite suite;

void setup(){
    Serial.begin(9600);
}

test(addition){
    assertEquals(3, 1 + 2);
}

void loop() {
    suite.run();
}
