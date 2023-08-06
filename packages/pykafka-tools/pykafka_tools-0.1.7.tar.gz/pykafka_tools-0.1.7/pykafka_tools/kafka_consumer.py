# -*- coding: utf-8 -*-

import logging
import os
import threading
import datetime
import time
import avro.io
import psycopg2
import pykafka.exceptions
from pykafka import KafkaClient
import pykafka_tools.event as event
from pykafka_tools.avro_coding import AvroCoding

__author__ = u'Stephan Müller'
__copyright__ = u'2017, Stephan Müller'
__license__ = u'MIT'

logger = logging.getLogger(__name__)


class KafkaConsumer(threading.Thread):
    """A KafkaConsumer is a thread which consumes messages and notifies functions by an event trigger after every new
     consumption.
     """

    def __init__(self, kafka_hosts, topic, consumer_group, kafka_message_schema_file=None, use_rdkafka=False,
                 auto_commit_enable=True, auto_commit_interval_ms=30000):
        """
        Initializes a new instance

        :param kafka_hosts: kafka hosts
        :type kafka_hosts: str
        :param topic: topic for which a consumer should being created
        :type topic: str
        :param consumer_group: consumer group
        :type consumer_group: str
        :param use_rdkafka: set true to use rdkafka
        :type use_rdkafka: bool
        :param auto_commit_enable: enable auto commit
        :type auto_commit_enable: bool
        :param auto_commit_interval_ms: auto commit interval in milliseconds
        :type auto_commit_interval_ms: int
        :param kafka_message_schema_file: kafka message schema. If messages are avro encoded, the schema is used to
               decode the messages.
        :type kafka_message_schema_file: file str
        """

        super().__init__(name='KafkaConsumer_' + topic)
        self._stopevent = threading.Event()
        self._topic = topic
        self._consumer_group = consumer_group
        self._kafka_hosts = kafka_hosts
        self._use_rdkafka = use_rdkafka
        self._auto_commit_enable = auto_commit_enable
        self._auto_commit_interval_ms = auto_commit_interval_ms
        self._avro_coding = None
        if kafka_message_schema_file is not None:
            if os.path.isfile(kafka_message_schema_file):
                self._avro_coding = AvroCoding(kafka_message_schema_file)

        self._consumer = None

        self.new_message_event = event.Event()

    def get_topic(self):
        """
        Get topic name
        :return: topic name
        :type: str
        """
        return self._topic

    def run(self):
        """ Thread loop. If establishing connection fails, a new connection try is performed every second.
        """

        while not self._stopevent.isSet():
            try:
                client = KafkaClient(hosts=self._kafka_hosts)
                topic = client.topics[str.encode(self._topic)]
                self._consumer = topic.get_simple_consumer(consumer_group=str.encode(self._consumer_group),
                                                           auto_commit_enable=self._auto_commit_enable,
                                                           auto_commit_interval_ms=self._auto_commit_interval_ms,
                                                           use_rdkafka=self._use_rdkafka)
                for message in self._consumer:
                    try:
                        if self._stopevent.isSet():
                            raise InterruptedError

                        if self._avro_coding is None:
                            message_data = message.value

                        else:
                            try:
                                message_data = self._avro_coding.decode(message.value)

                            except (AssertionError, IndexError, avro.io.SchemaResolutionException):
                                logger.warning("Could not parse message with offset " + str(message.offset) +
                                               " of topic '" + self._topic + "'. Continuing.")
                                continue

                        log_message = "Received message from topic " + self._topic + " with offset "\
                                      + str(message.offset)
                        if type(message_data) == dict and "timestamp" in message_data:
                            log_message += " and timestamp " + datetime.datetime.fromtimestamp(
                                message_data["timestamp"]).strftime('%Y-%m-%d %H:%M:%S.%f')

                        logger.info(log_message)

                        self.new_message_event.fire(self, message_data)

                    except pykafka.exceptions.ConsumerStoppedException:
                        logger.warning("Consumer for topic " + self._topic + " was stopped manually.")

                    except Exception as e:
                        logger.exception(e)

            except pykafka.exceptions.ConsumerStoppedException:
                logger.warning("Consumer for topic " + self._topic + " was stopped manually.")

            except Exception as e:
                logger.exception(e)
                time.sleep(1)

    def stop(self):
        self._stopevent.set()
        if self._consumer is not None:
            self._consumer.stop()

    def join(self, timeout=None):
        """
        Stop the thread loop and wait for it to end.

        :param timeout: timeout
        :type timeout: float
        """
        self.stop()
        super().join(timeout)


class DBWriter(KafkaConsumer):

    def __init__(self, kafka_hosts, topic, consumer_group, kafka_message_schema_file, postgres_connector,
                 use_rdkafka=False, auto_commit_enable=True, auto_commit_interval_ms=30000):

        super().__init__(kafka_hosts, topic, consumer_group, kafka_message_schema_file, use_rdkafka,
                         auto_commit_enable, auto_commit_interval_ms)

        if self._avro_coding is None:
            raise IOError("Kafka message schema file does not exist.")

        self._postgres_connector = postgres_connector
        self.new_message_event += self._new_message_handler
        self._parsed_first_message_correctly = False

    def _new_message_handler(self, sender, message):

        try:
            if not self._parsed_first_message_correctly:
                # create or update table schema if necessary
                if not self._postgres_connector.table_exists(self._topic):
                    self._postgres_connector.create_table(table_name=self._topic, data=message["data"])
                    logger.info("Created table for topic '" + self._topic + "'")

                else:
                    number_of_added_columns = self._postgres_connector.update_columns(table_name=self._topic,
                                                                                      data=message["data"])
                    logger.info("Added " + str(number_of_added_columns) + " columns in table for topic '" + self._topic + "'")
                self._parsed_first_message_correctly = True

            self._postgres_connector.insert_values(table_name=self._topic, data=message)

        except psycopg2.OperationalError:
            raise ConnectionError("Postgres operational error.")

        except:
            # TODO not a nice way, because another exception is thrown
            self.join(0)
