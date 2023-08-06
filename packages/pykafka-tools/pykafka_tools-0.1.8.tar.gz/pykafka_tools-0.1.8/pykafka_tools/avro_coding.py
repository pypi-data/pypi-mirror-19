#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import avro
import avro.io

__author__ = u'Stephan Müller'
__copyright__ = u'2017, Stephan Müller'
__license__ = u'MIT'


class AvroCoding(object):

    def __init__(self, kafka_message_schema_file):
        self._kafka_message_schema = avro.schema.Parse(open(kafka_message_schema_file, "rb").read().decode())

    def decode(self, message):
        bytes_reader = io.BytesIO(message)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(self._kafka_message_schema)
        return reader.read(decoder)

    def encode(self, message):
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer = avro.io.DatumWriter(self._kafka_message_schema)
        writer.write(message, encoder)
        return bytes_writer.getvalue()
