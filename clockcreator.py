from datetime import datetime, timedelta
from psd_tools import PSDImage
from PIL.Image import Image
import config
import pytz


class ClockCreator:
    def __init__(self):
        self.psd = PSDImage.open(config.CLOCK_SOURCE_PATH)

    def create_next(self):
        self.hours, self.minutes = self._get_time_layers()
        next_hour, next_minute = ClockCreator._get_time()

        self._create_next_clock(next_hour, next_minute)

    def _create_next_clock(self, next_hour, next_minute):
        self._set_layers_visibility(next_hour, next_minute, True)
        self._save_clock()
        self._set_layers_visibility(next_hour, next_minute, False)

    def _save_clock(self):
        image: Image = self.psd.composite()
        image.save(config.CLOCK_PATH)

    def _set_layers_visibility(self, hour, minute, visibility):
        for i in range(2):
            self.hours[i][int(hour[i])].visible = visibility
            self.minutes[i][int(minute[i])].visible = visibility

    @staticmethod
    def _get_time():
        timezone = pytz.timezone(config.TIME_ZOME)

        time = datetime.time(datetime.now(timezone) + timedelta(minutes=1)).strftime("%H:%M")
        next_hour, next_minute = time.split(":")

        return next_hour, next_minute

    def _get_time_layers(self):
        hours = self.psd[5:3:-1]
        minutes = self.psd[2:0:-1]

        return hours, minutes
