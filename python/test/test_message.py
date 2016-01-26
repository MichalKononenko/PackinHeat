"""
Contains unit tests for :mod:`python_src.message_handler`
"""
import unittest
import struct
from python.src.message_handling import SerialMessage, BadPacketError

__author__ = 'Michal Kononenko'


class TestMessage(unittest.TestCase):
    def setUp(self):
        self.packet_number = 1
        self.number_of_packets = 1
        self.instruction = 1
        self.data = bytes('foo'.encode('ascii'))

    def _assert_constructor_parameters(self, message):
        self.assertIsInstance(message, SerialMessage)
        self.assertEqual(message.packet_number, self.packet_number)
        self.assertEqual(message.number_of_packets, self.number_of_packets)
        self.assertEqual(message.data, self.data)
        self.assertEqual(message.response, [])


class TestMessageConstructor(TestMessage):
    def test_constructor(self):
        message = SerialMessage(self.packet_number, self.number_of_packets,
                                self.instruction, self.data
                                )

        self._assert_constructor_parameters(message)


class TestFromFormatDict(TestMessage):
    def setUp(self):
        TestMessage.setUp(self)
        self.format_dict = \
            {
                "ID": self.packet_number,
                "NUMBER_OF_PACKETS": self.number_of_packets,
                "INSTRUCTION": self.instruction,
                "DATA": bytes('foo'.encode('ascii'))
            }

    def test_format_dict_constructor(self):
        message = SerialMessage.from_format_dict(self.format_dict)

        self._assert_constructor_parameters(message)


class TestWithConstructedMessage(TestMessage):
    """
    Tests that the datagram length is 64 bytes
    """
    def setUp(self):
        TestMessage.setUp(self)
        self.expected_datagram_length = 64

        self.message = SerialMessage(
            self.packet_number, self.number_of_packets, self.instruction,
            bytes('foo'.encode('ascii'))
        )

    def test_datagram(self):
        packet = self.message.datagram
        self.assertEqual(len(packet), 64)

        self.assertEqual(
                [self.packet_number, self.number_of_packets,
                 self.instruction], self._deconstruct_packet(packet))

    @staticmethod
    def _deconstruct_packet(packet):
        packet_number = struct.unpack('>H', packet[0:2])
        number_of_packets = struct.unpack('>H', packet[2:4])
        instruction = struct.unpack('>H', bytes(packet[4:6]))

        return [x[0] for x in (packet_number, number_of_packets, instruction)]


class TestFromByteStream(TestWithConstructedMessage):
    def setUp(self):
        TestWithConstructedMessage.setUp(self)
        self.byte_streamed_message = self.message.datagram

    def test_from_byte_stream(self):
        message = SerialMessage.from_byte_stream(self.byte_streamed_message)
        self.assertEqual(message.datagram, self.message.datagram)

    def test_bad_packet_length(self):
        bad_message = self.byte_streamed_message + b'foo'
        self.assertNotEqual(len(bad_message), len(self.byte_streamed_message))

        with self.assertRaises(BadPacketError):
            SerialMessage.from_byte_stream(bad_message)
