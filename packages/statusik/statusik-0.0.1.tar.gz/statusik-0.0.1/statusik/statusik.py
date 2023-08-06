import datetime
import json
import sys
import threading
import time

from abc import abstractmethod

from test.test_isinstance import AbstractClass


class Plugin(object):
    __metaclass__ = AbstractClass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_full_text(self):
        pass

    @abstractmethod
    def get_color(self):
        pass

    @abstractmethod
    def process(self):
        pass


class DateTimePlugin(Plugin):
    def __init__(self):
        self.counter = 0

    def get_full_text(self):
        full_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return full_text

    def get_name(self):
        return "date-time-plugin"

    def get_color(self):
        return "#ffffff"

    def process(self):
        self.counter += 1


def eprint(*args, **kwargs):
    print(file=sys.stderr, *args, **kwargs)


def print_header():
    header = {"version": 1, "click_events": True}
    print(json.dumps(header))


def print_events():
    for event in sys.stdin:
        if event.startswith('['):
            continue
        eprint(event)


plugins = [DateTimePlugin()]


def infinite_loop():
    print("[[]")
    counter = 0
    while True:
        counter += 1
        payloads = []

        for plugin in plugins:
            payloads.append(
                {
                    "name": plugin.get_name(),
                    "full_text": plugin.get_full_text(),
                    "color": plugin.get_color()
                }
            )
            plugin.process()

        print("," + json.dumps(payloads))
        time.sleep(1)
        sys.__stdout__.flush()


class ClickEventHandler(threading.Thread):
    def run(self):
        for line in sys.stdin:
            eprint(line)
            sys.__stderr__.flush()


click_event_handler = ClickEventHandler()
click_event_handler.start()

print_header()
infinite_loop()
