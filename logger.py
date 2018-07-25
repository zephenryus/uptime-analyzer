import datetime
import threading
import time

import requests


class Logger:
    def __init__(self):
        self.domain = ''
        self.timeout_time = 10
        self.running = False
        self.log_file = 'log.txt'

    def start(self, domain: str, override_time=0):
        self.domain = domain

        if override_time is not 0:
            self.timeout_time = override_time

        self.running = True
        self.loop()

    def loop(self):
        if self.is_running():
            self.log_response(self.get_response())
            threading.Timer(self.timeout_time, self.loop).start()

    def is_running(self):
        return self.running

    def get_response(self):
        try:
            response = requests.head(self.domain)
            return response.status_code
        except requests.ConnectionError:
            print("failed to connect")
            return 'Could not connect (Local error)'

    def log_response(self, status):
        with open(self.log_file, 'a+') as logfile:
            now = datetime.datetime.now()
            print("{0} - {1}".format(str(now), str(status)))
            logfile.write("{0}\t{1}\t{2}\n".format(int(time.mktime(now.timetuple())), str(now), str(status)))


def main():
    logger = Logger()
    logger.start('https://willisworksstudio.com/', 300)


if __name__ == "__main__":
    main()
