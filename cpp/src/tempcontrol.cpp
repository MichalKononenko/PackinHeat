/**
* Contains a reimplementation of the Tempcontroller protocols
* using more C++ features to optimize language use
*/
#include <Arduino.h>
#define PACKET_SIZE 64
#define PACKET_TRANSFER_RATE 9600
#define POWER_PIN 10

typedef unsigned char byte;

/**
* All variables related to communication will go here for now
*/
namespace communication {
  /**
  * Reads a packet of the required size in bytes, and returns a pointer to the
  * packet.
  */
  unsigned char *read_buffer(int packet_size){
    int buffer_length = packet_size--;

    byte *buffer = new byte[buffer_length];
    buffer = Serial.readBytes(buffer, buffer_length);

    return &buffer;
  };

  class PacketHeader:
  {
  public:
    unsigned short int get_packet_id;
    unsigned short int get_number_of_packets;
    unsigned short int get_instruction;
    unsigned short int get_length_of_data;
  private:
    unsigned char *buffer;
  }
}

const int input_pins[] = [1, 2, 3, 4, 5, 6, 7, 8];


void setUp()
{
 pinMode(POWER_PIN, OUTPUT);
 Serial.begin(PACKET_TRANSFER_RATE);

}
