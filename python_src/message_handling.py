"""
Contains a class for creating and recieving serial messages
"""
import struct
import os
from bitstring import BitArray

SHORT_INT = {'minimum': 0, 'maximum': 65535}


class BadPacketError(ValueError):
    pass


class SerialMessage(object):
    _id_type = SHORT_INT
    _number_of_messages_type = SHORT_INT
    _code_type = SHORT_INT

    packet_size = 64
    checksum_size = 8

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
                   info_dict['INSTRUCTION'], info_dict['DATA'])

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
        Calculates the checksum for a set of 63 bytes.
        :return:
        """
        data_to_check = self._header + self.data + self._padding
        check_bits = ''.join(
                map(str, map(self._calculate_parity_bit, data_to_check))
        )

        unchecked_bytes = BitArray(bin=check_bits).tobytes()

        unchecked_bytes_checksum = ''.join(
                map(str, map(self._calculate_parity_bit, unchecked_bytes))
        )

        check_byte = BitArray(bin=unchecked_bytes_checksum).tobytes()

        return unchecked_bytes + check_byte

    @staticmethod
    def _calculate_parity_bit(byte):
        """
        Calculate the parity bit for a byte
        :param bytes byte: The byte for which to calculate the parity bit
        :return:
        """
        return byte % 2

    @property
    def _padding(self):
        current_packet_size = \
            len(self._header) + self.checksum_size + len(self.data)

        required_length = self.packet_size - current_packet_size

        if len(self._padding_bytes) != required_length:
            self._padding_bytes = os.urandom(required_length)
        return self._padding_bytes

    @_padding.setter
    def _padding(self, padding_to_set):
        self._padding_bytes = padding_to_set

    @classmethod
    def from_byte_stream(cls, packet_bytes):
        if len(packet_bytes) != cls.packet_size:
            raise BadPacketError(
                    'The packet to be processed is not %d bytes long',
                    cls.packet_size
            )

        parsed_byte_stream = cls.parse_byte_stream(packet_bytes)

        message = cls(parsed_byte_stream['packet_number'],
                      parsed_byte_stream['number_of_packets'],
                      1, parsed_byte_stream[
                          'data'])

        message._padding = parsed_byte_stream['padding']

        if message._checksum != parsed_byte_stream['checksum']:
            raise BadPacketError('An error was detected in the packet')
        else:
            return message

    @classmethod
    def parse_byte_stream(cls, byte_stream):

        header = byte_stream[0:8]
        packet_number, number_of_packets, instruction, data_length = \
            struct.unpack('>HHHH', header)

        data = byte_stream[8:8+data_length]

        padding_length = cls.packet_size - cls.checksum_size - \
                         data_length - len(header)

        padding = byte_stream[8+data_length:8+data_length+padding_length]

        checksum = byte_stream[8+data_length+padding_length:cls.packet_size]

        return dict(
                packet_number=packet_number,
                number_of_packets=number_of_packets,
                instruction=instruction,
                data=data,
                padding=padding,
                checksum=checksum
                )
