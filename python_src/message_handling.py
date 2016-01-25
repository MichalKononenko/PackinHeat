import struct
import random
import serial
import os

SHORT_INT = {'minimum': 0, 'maximum': 65535}


class SerialMessage(object):
    _id_type = SHORT_INT
    _number_of_messages_type = SHORT_INT
    _code_type = SHORT_INT

    _packet_size = 64
    _checksum_size = 8

    def __init__(
            self, packet_number, number_of_packets, instruction_number, data
    ):
        self.packet_number = packet_number
        self.number_of_packets = number_of_packets
        self.instruction = instruction_number
        self.data = data
        self.response = []
        self._padding_bytes = bytes()

    @classmethod
    def from_format_dict(cls, info_dict):
        return cls(info_dict['ID'], info_dict['NUMBER_OF_PACKETS'],
                   info_dict['INSTRUCTION'], info_dict['data'])

    @property
    def datagram(self):
        return self._header + self.data + self._padding + self._checksum

    @property
    def _header(self):
        """
        Creates the instruction header, composed of four short ints. These are

            -   The number of the packet to be sent
            -   The number of packets in the set
            -   The instruction code
            -   The length of the data to be sent

        :return: A byte string representing the _header of the message
        :rtype: bytes
        """
        return struct.pack(
            '>HHHH', self.packet_number, self.number_of_packets,
            self.instruction, len(self.data)
        )

    @property
    def _checksum(self):
        """
        Calculates the checksum for a given set of
        :return:
        """
        return ''

    @property
    def _padding(self):
        current_packet_size = \
            len(self._header) + self._checksum_size + len(self.data)

        required_length = self._packet_size - current_packet_size

        if len(self._padding_bytes) != required_length:
            self._padding_bytes = os.urandom(required_length)
        return self._padding_bytes

    def send(self, output_serializer=serial.Serial('COM1')):
        with output_serializer as ser:
            ser.write(self.datagram)
