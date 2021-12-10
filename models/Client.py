"""
This module have the class Client
for model a client of the server.
"""

import sys
from typing import Type
sys.path.append('.')

from settings.ips_allows import IP_ALLOWS
from models.Ip import Ip

class Client:
  """
  Create a client with a ip address.
  """

  bits_limits = 12

  def __init__(self, ipAddress:str) -> None:
      # validating the ip for raise a exception
      if type(ipAddress) not in [str]:
        raise TypeError(f'The ip {ipAddress} passed for parameter must be a string. Not a -- {type(ipAddress)} --')

      if len(ipAddress.split('.')) > self.bits_limits:
        raise TypeError(f'The ip length {ipAddress} passed for parameter is mayor to 12. Must be 8 bits for each block.')

      # initial value for the Client object
      self.ipAddress = ipAddress

  def validate_client(self) -> bool:
    """
    Return True if the ip
    of the client created is in the range
    of the ips allows.

    """

    first_ip = Ip(IP_ALLOWS[0])
    second_ip = Ip(IP_ALLOWS[1])
    first_last_block = first_ip.get_block(4)
    second_last_block = second_ip.get_block(4)

    range_ips = [ip for ip in range(first_last_block, second_last_block + 1)]

    if int(self.ipAddress.split('.')[3]) in range_ips:
      return True

    return False


  def __str__(self) -> str:
      return f'This is a client with ip {self.ipAddress}'