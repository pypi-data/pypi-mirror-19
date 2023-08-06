from .config import battery_dir
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Smapi(object):

    def __init__(self):
        logger.debug(self.__class__.__name__ + ' info module initialized')

    def __str__(self):
        return str(self.__dict__)

    def refresh(self):
        self.set_battery()

    def set_battery(self):
        files = [
            'state',
            'remaining_percent',
            'power_avg',
            'cycle_count',
            'remaining_running_time',
            'stop_charge_thresh',
        ]
        for filename in files:
            with open(battery_dir + filename, 'r') as f:
                try:
                    setattr(self, filename, f.read().replace('\n', ''))
                except FileNotFoundError:
                    raise
