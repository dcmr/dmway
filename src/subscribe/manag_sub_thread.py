import json
import sys
import threading

from src.subscribe.subscribe import SubThread


class ManagSubThread:
    def __init__(self, p):
        self.__p = p
        self.broker = {}
        self.threads_list = []

    def set_json_broker_default(self):
        try:
            with open(self.__p.file_dict["broker.json"]) as json_mqtt_broker:
                self.broker = json.load(json_mqtt_broker)
        except FileNotFoundError as file_not_found:
            print(file_not_found)
        except json.decoder.JSONDecodeError as wrong_json_format:
            print(wrong_json_format)

    def create_sub_threads(self):
        for k, v in self.broker['mqtt'].items():
            t = SubThread(self.broker['mqtt'][k]['ip'], self.broker['mqtt'][k]['topic'], self.__p)
            self.threads_list.append(t)

    def start_threads(self):
        for t in self.threads_list:
            t.start()

    def signal_handler(self, sig, frame):
        try:
            print("Cleaning process")
            for t in self.threads_list:
                t.client.stop_running()
                t.join()
        except:
            pass
        sys.exit(0)

    def start(self):
        self.set_json_broker_default()
        self.create_sub_threads()
        self.start_threads()
