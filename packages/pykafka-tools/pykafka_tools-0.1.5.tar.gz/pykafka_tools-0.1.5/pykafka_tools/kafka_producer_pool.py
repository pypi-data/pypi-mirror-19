# -*- coding: utf-8 -*-

import logging
import os
from threading import Thread
import avro.io
from pykafka import KafkaClient
import pykafka.exceptions
from pykafka_tools.avro_coding import AvroCoding

__author__ = u'Stephan Müller'
__copyright__ = u'2017, Stephan Müller'
__license__ = u'MIT'

logger = logging.getLogger(__name__)


class KafkaProducerPool(object):
    """
    Manages connection to Kafka and is responsible for producing messages. Holds a cache of messages if connection
    to Kafka is lost and send them after connection is established again.
    """

    def __init__(self, kafka_hosts, topics, kafka_message_schema_file=None, use_rdkafka=False, sync=True):
        """
        Instantiate a new KafkaProducerPool and tries to connect to Kafka

        :param kafka_hosts: kafka hosts
        :type kafka_hosts: str
        :param topics: list of topics for which a producer should being created
        :type topics: list of str
        :param use_rdkafka: set true to use rdkafka
        :type use_rdkafka: bool
        :param sync: If true, directly sends messages to Kafka
        :type sync: bool
        """
        self._kafka_hosts = kafka_hosts
        self._topic_names = topics
        self._use_rdkafka = use_rdkafka
        self._sync = sync
        self._avro_coding = None
        if kafka_message_schema_file is not None:
            if os.path.isfile(kafka_message_schema_file):
                self._avro_coding = AvroCoding(kafka_message_schema_file)

        self._client = None
        self._topics = dict()
        self._producers = dict()
        self._connected = False
        self._try_reconnect = False
        self._producer_is_working = False
        self._producer_messages = dict()
        for topic in topics:
            self._producer_messages.update({
                topic: list()
            })
        self.connect()

    def _reset(self):
        """
        Delete all Kafka clients, topics and producers. Call this method after connection was lost.
        """
        self._client = None
        self._topics = dict()
        self._producers = dict()

    def connect(self):
        """
        Tries to connect to Kafka by creating a new thread so that main thread is not being blocked.
        On successful connection, producers for selected topics are created.
        """
        if self._try_reconnect is False:
            logger.debug("Try connecting.")

            def connect_thread():
                self._try_reconnect = True
                try:
                    self._client = KafkaClient(hosts=self._kafka_hosts)
                    for topic_name in self._topic_names:
                        self._topics.update({
                            topic_name: self._client.topics[topic_name.encode()]
                        })
                        self._producers.update({
                            topic_name:
                                self._topics[topic_name].get_producer(use_rdkafka=self._use_rdkafka, sync=self._sync)
                        })
                    self._connected = True
                except Exception as e:
                    self._reset()
                    logger.exception(e)
                self._try_reconnect = False

            thread = Thread(target=connect_thread)
            thread.start()
        else:
            logger.debug("Already tries to connect.")

    def produce(self, topic, message):
        """
        Collects messages to produce and triggers a new thread to actually send messages so that main thread will
        not being blocked.

        :param topic: topic name
        :type topic: str
        :param message: message
        :type message: str or bytes or dict
        """
        try:
            if type(message) is bytes:
                pass
            if type(message) is dict and self._avro_coding is not None:
                try:
                    message = self._avro_coding.encode(message)

                except (AssertionError, IndexError, avro.io.SchemaResolutionException):
                    logger.warning("Could not parse message of topic '" + topic + "'. Continuing.")
                    return
            else:
                message = str(message).encode()

            self._producer_messages[topic].append(message)

        except KeyError:
            raise KeyError("Producer for given topic '" + topic + "' is not initialized. Please make sure that all"
                           " desired topics are listed in KafkaProducerPool.__init__()")
        if self._connected is False and self._try_reconnect is True:
            logger.debug("Not connected to Kafka but still trying to connect.")
        elif self._connected is False:
            self.connect()
        else:
            def produce_thread():
                self._producer_is_working = True
                sent_messages_count = 0
                processed_messages_count = 0
                try:
                    for topic_name in self._producer_messages:
                        while len(self._producer_messages[topic_name]) > 0:
                            processed_messages_count += 1
                            self._producers[topic_name].produce(self._producer_messages[topic_name][0])
                            self._producer_messages[topic_name].pop(0)
                            sent_messages_count += 1
                except pykafka.exceptions.NoBrokersAvailableError:
                    self._connected = False
                    logger.error("Disconnected because connection to brokers could not be established.")
                except pykafka.exceptions.RdKafkaException as e:
                    self._connected = False
                    logger.error(e)
                except Exception as e:
                    logger.exception(e)
                    raise
                finally:
                    self._producer_is_working = False
                    logger.info("Sent %s of %s messages successful to Kafka.", sent_messages_count,
                                processed_messages_count)

            if not self._producer_is_working:
                thread = Thread(name='Producer', target=produce_thread)
                thread.start()
            else:
                logger.debug("Another produce thread is still working.")
