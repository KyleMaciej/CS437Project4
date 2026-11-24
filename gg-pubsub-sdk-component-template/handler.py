
'''
my_system_message_handler.py
'''

import logging, random
from process_emissions import process_emissions
 
# Config the logger.
log = logging.getLogger(__name__)

class MySensorMessageHandler():
  
  def __init__(self, publish_message, publish_error, message_formatter):
        '''
        A common patten when receiving a PubSub message is to create and publish a response
        so we in this example we pass a reference to the PubSub SDK publish_message, publis_error callbacks 
        and message_formatter object.

        '''
        self.publish_message = publish_message
        self.publish_error = publish_error
        self.message_formatter = message_formatter

  def process(self, protocol, topic, message_id, status, route, message):

    msg = process_emission(message)
    response = self.message_formatter.get_message(
      message_id=message_id,
      route="emissions_route",
      message=msg
    )
    self.publish_message(protocol=protocol, message=response)
