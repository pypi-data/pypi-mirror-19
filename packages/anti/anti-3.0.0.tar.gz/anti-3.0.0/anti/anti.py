# -*- coding:utf-8 -*-

import pika
import redis
import logging
import urlparse


try:
    from django.conf import settings
except ImportError:
    import config as settings
from bs4 import BeautifulSoup

from .mixin import openYandexMixin
from .utils import get_redis_key, wait_redis_urls

FORMAT = '[%(asctime)-15s] // %(message)s'
LEVEL = logging.DEBUG if getattr(settings, 'DEBUG', False) else logging.WARNING
logging.basicConfig(format=FORMAT, level=LEVEL)


class openYandex(openYandexMixin):
    def __init__(self):
        self.rds = redis.Redis(**settings.ANTI_REDIS_CONF)
        self.connect()

    def connect(self):
        connection = pika.BlockingConnection(pika.URLParameters(settings.ANTI_AMQP_CONF))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='main')

    def restart_browser(self):
        self.channel.basic_publish(
            exchange='',
            routing_key='main',
            body='###restart###',
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def run_task(self, url):
        self.channel.basic_publish(
            exchange='',
            routing_key='main',
            body=url,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def get_soup(self, url, cache=True, timeout=120):
        redis_key = get_redis_key(self.rds, url)
        parse_url = urlparse.urlparse(url)
        self.query = parse_url.query.encode('utf8') if isinstance(parse_url.query, unicode) else parse_url.query
        if cache and self.rds.get(redis_key):
            return BeautifulSoup(self.rds.get(redis_key), 'html.parser')
        else:
            self.rds.set(redis_key, '')
            self.run_task(url)
            wait_redis_urls(self.rds, url, timeout)
        return BeautifulSoup(self.rds.get(redis_key), 'html.parser')

openGoogle = openYandex
