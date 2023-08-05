# -*- coding: utf-8 -*-

import logging
from threading import Thread
from pykafka import KafkaClient
import pykafka.exceptions

__author__ = u'Stephan Müller'
__copyright__ = u'2016, Stephan Müller'
__license__ = u'MIT'

log = logging.getLogger(__name__)


class KafkaProducerPool(object):
    """
    Manages connection to Kafka and is responsible for producing messages. Holds a cache of messages if connection
    to Kafka is lost and send them after connection is established again.
    """

    def __init__(self, kafka_hosts, topics, use_rdkafka=False, sync=True):
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
            log.debug("Try connecting.")

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
                    log.error(e)
                self._try_reconnect = False

            thread = Thread(target=connect_thread)
            thread.start()
        else:
            log.debug("Already tries to connect.")

    def produce(self, topic, message):
        """
        Collects messages to produce and triggers a new thread to actually send messages so that main thread will
        not being blocked.

        :param topic: topic name
        :type topic: str
        :param message: message
        :type message: bytes
        """
        if type(message) is not bytes:
            log.warning("Message from topic " + topic + " is not of type byte and will be ignored. Continue.")
            return
        try:
            self._producer_messages[topic].append(message)
        except KeyError:
            raise KeyError("Producer for given topic '" + topic + "' is not initialized. Please make sure that all"
                           " desired topics are listed in KafkaProducerPool.__init__()")
        if self._connected is False and self._try_reconnect is True:
            log.debug("Not connected to Kafka but still trying to connect.")
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
                    log.error("Disconnected because connection to brokers could not be established.")
                except pykafka.exceptions.RdKafkaException as e:
                    self._connected = False
                    log.error(e)
                except Exception as e:
                    log.exception(e)
                    raise
                finally:
                    self._producer_is_working = False
                    log.info("Sent %s of %s messages successful to Kafka.", sent_messages_count,
                             processed_messages_count)

            if not self._producer_is_working:
                thread = Thread(name='Producer', target=produce_thread)
                thread.start()
            else:
                log.debug("Another produce thread is still working.")
