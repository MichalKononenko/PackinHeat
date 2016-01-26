#include ".\packet.hpp"
#ifndef PACKET_SIZE
#define PACKET_SIZE 64
#endif

packet::Header::Header(byte *buffer_address){
  *buffer = *buffer_address;
}

unsigned short int packet::Header::get_packet_id(void){
  unsigned char packet_id_data = [buffer[0], buffer[1]];
  unsigned short int packet_id;
  memcpy(&packet_id, packet_id_data, sizeof(packet_id));

  return packet_id;
}
