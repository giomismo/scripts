import time
import re
import sys
import os
import RPi.GPIO as GPIO


class PowerManagerScheduler:

    def __init__(self, config_file, standalone_run=False):
        self._sleep_time = 60
        self._config_file = config_file
        self.config = {}
        self.GPIOMgr = GPIOManager(self.read_config()["gpio"])
        if standalone_run:
            try:
                self.standalone()
            except KeyboardInterrupt:
                print "Control+C detected, cleaning GPIO and exiting."
                self.GPIOMgr.cleanup()

    def standalone(self):
        while True:
            self.process()
            time.sleep(self._sleep_time)

    def process(self):
        [dow, hour, minute] = time.strftime("%A,%H,%M").split(",")
        print "*** Checking: {} - {}:{}".format(dow, hour, minute)

        self.config = self.read_config()
        if not self.GPIOMgr.gpio_number == self.config["gpio"]:
            self.GPIOMgr.update_gpio_number(self.config["gpio"])

        if self.config["always_on"]:
            print "** Alaways on is active"
            self.GPIOMgr.activate()
        else:
            print "** Checking schedule:"
            self.activate_depending_on_schedule(dow, hour, minute)

    def read_config(self):
        with open(self._config_file) as fr:
            content = fr.read()

        config = {}
        config["always_on"] = re.findall("always_on=([0-9]*)\n", content)[0] == "1"
        config["gpio"] = int(re.findall("gpio=([0-9]*)\n", content)[0])
        for dow in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            config[dow] = re.findall("{}=([^\n]*)".format(dow), content)[0].split(",")
        return config

    def activate_depending_on_schedule(self, dow, hour, minute):
        hour = int(hour)
        minute = int(minute)
        current_hour_minutes_in_minutes = hour*60 + minute
        print "* Time frames for {}: {}".format(dow, self.config[dow.lower()])

        for time_frame in self.config[dow.lower()]:
            [min_hour_min, max_hour_min] = time_frame.split("-")
            [min_hour, min_minute] = map(lambda x: int(x), min_hour_min.split(":"))
            min_hour_minutes_in_minutes = min_hour*60 + min_minute
            [max_hour, max_minute] = map(lambda x: int(x), max_hour_min.split(":"))
            max_hour_minutes_in_minutes = max_hour*60 + max_minute

            print "* Checking {} <= {}:{} <= {}".format(min_hour_min, hour, minute, max_hour_min)
            if min_hour_minutes_in_minutes <= current_hour_minutes_in_minutes <= max_hour_minutes_in_minutes:
                print "* Matched, activated"
                self.GPIOMgr.activate()
                return
        print "* Not matched, deactivating"
        self.GPIOMgr.deactivate()
        return


class GPIOManager:
    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.start()

    def start(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_number, GPIO.OUT)

    def activate(self):
        if not self._is_gpio_active(self.gpio_number):
            GPIO.output(self.gpio_number, GPIO.HIGH)

    def deactivate(self):
        if self._is_gpio_active(self.gpio_number):
            GPIO.output(self.gpio_number, GPIO.LOW)

    def update_gpio_number(self, new_number):
        if not self.gpio_number == new_number:
            self.cleanup()
            self.gpio_number = new_number
            self.start()

    @staticmethod
    def _is_gpio_active(gpio_number):
        return GPIO.input(gpio_number) == GPIO.HIGH

    @staticmethod
    def cleanup():
        GPIO.cleanup()


def usage():
    print "Usage: {} <config_file>\n" \
          "\n" \
          "Config file example:\n" \
          "always_on=0\n" \
          "gpio=18\n" \
          "monday=09:00-16:00\n" \
          "tuesday=09:00-16:00\n" \
          "wednesday=09:00-16:00\n" \
          "thursday=09:00-16:00\n" \
          "friday=09:00-16:00\n" \
          "saturday=09:00-16:00\n" \
          "sunday=09:00-16:00\n" \
          "\n" \
          "Config file format:\n" \
          " - always_on: 0 for activate/deactivate gpio based on schedule, 1 to keep gpio activated always\n" \
          " - gpio: gpio number to activate/deactiveate (based on BOARD number)\n" \
          " - day of week: accepts multiple time schedules comma separated\n" \
          "    - example 1: monday=01:23-12:34\n" \
          "    - example 2: monday=01:23-12:34,13:37-20:00,21:43-23:45"

if __name__ == "__main__":
    if not len(sys.argv) == 2 or os.path.exists(sys.argv[1]):
        usage()
        sys.exit()
    PMS = PowerManagerScheduler(sys.argv[1], standalone_run=True)
