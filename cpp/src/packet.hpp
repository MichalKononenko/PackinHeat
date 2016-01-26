/**
* Contains modules for working with packets delivered by serial connection.
*
*
*/
#ifndef PACKET_H
#define PACKET_H

#ifndef byte
typedef unsigned char byte;
#endif

namespace packet {
  class Header {
  public:
    Header(byte *buffer_address);
    unsigned short int get_packet_id;
    unsigned short int get_number_of_packets;
    unsigned short int get_instruction;
    unsigned short int get_length_of_data;
    byte get_data;
  private:
    byte *buffer;
  };
};

#endif
