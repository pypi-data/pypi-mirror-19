from pprint import pprint
import logging
import asyncio

from .config import stop_thresh_charging
from .config import stop_thresh_idle
from .config import thresh_file
from .config import charge_change

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Action(object):
    def __init__(self):
        logger.debug(self.__class__.__name__ + ' action module initialized')

    async def run(self, data):
        logger.error(self.__class__.__name__ + ' run not implemented')


class Dumper(Action):
    async def run(self, data):
        await asyncio.sleep(0.2)
        pprint(data)


class Charging(Action):
    def get_state(self):
        """Return current state"""

        if int(self.smapi['stop_charge_thresh']) < stop_thresh_charging:
            return 'charging-disabled'
        elif int(self.smapi['stop_charge_thresh']) == stop_thresh_charging:
            return 'charging-enabled'

        return 'unknown-state'

    def set_state(self, state):
        logger.debug('Requested state: {}'.format(state))

        if state == 'charging-enabled':
            value = stop_thresh_charging
        elif state == 'charging-disabled':
            value = stop_thresh_idle

        if value:
            with open(thresh_file, 'w') as f:
                f.write(str(value))

    def transition(self):
        """Check and make transition"""
        state = self.get_state()
        logger.debug('state is ' + state)

        if state == 'charging-disabled':
            if (int(self.smapi['remaining_percent']) <= charge_change and
                    int(self.smapi['stop_charge_thresh']) <= stop_thresh_charging):
                self.set_state('charging-enabled')
                logger.debug('Move to state charging-enabled')

        elif state == 'charging-enabled':
            if self.smapi['state'] == 'idle':
                self.set_state('charging-disabled')
                logger.debug('Move to state charging-disabled')

        else:
            logger.error('Unknown state')

    async def run(self, data):
        try:
            self.smapi = data['Smapi']
        except AttributeError:
            print(data)
            raise

        try:
            self.transition()
        except:
            logger.error('transition failed')
            raise


# class Reporter(object):
#     """Reports information via MQTT"""
#
#     def __init__(self, **kwargs):
#         """
#         kwargs:
#             server
#             port
#             user
#             password
#         """
#
#         # set variables
#         self.logger = logging.getLogger(__name__)
#         self.server = kwargs.get('server')
#         self.port = kwargs.get('port', 1883)
#         self.user = kwargs.get('user')
#         self.password = kwargs.get('password')
#
#         # debug
#         self.logger.debug('Initialized with: {}'.format(self.__dict__))
#
#
#         # connect to mqtt broker
#         self.client = mqtt.Client()
#         self.client.username_pw_set(self.user, password=self.password)
#         self.client.connect(self.server, port=self.port)
#
#
#     def pub(self, topic, msg=None, retain=False):
#         self.client.publish(topic, payload=msg, retain=retain)
#         self.logger.debug(
#             'Published {}: {}'.format(topic, msg)
#         )
