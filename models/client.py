"""
This module have the class Client
for model a client of the server.
"""

import sys
from typing import Type
sys.path.append('.')

from settings.ips_allows import IP_ALLOWS
from models.ip import Ip

class Client:
  """
  Create a client with a ip address.
  """

  bits_limits = 12 # linits of bttes for use

  def __init__(self, ipAddress:str) -> None:
      # validating the ip for raise a exception
      if type(ipAddress) not in [str]:
        raise TypeError(f'The ip {ipAddress} passed for parameter must be a string. Not a -- {type(ipAddress)} --')

      if len(ipAddress.split('.')) > self.bits_limits:
        raise TypeError(f'The ip length {ipAddress} passed for parameter is mayor to 12. Must be 8 bits for each block.')

      # initial value for the Client object
      self.ipAddress = ipAddress

  def validate_client_for_range(self) -> bool:
    """
    Return True if the ip
    of the client created is in the range
    of the ips allows.

    """

    # getting values for validate
    first_ip = Ip(IP_ALLOWS[0])
    second_ip = Ip(IP_ALLOWS[1])
    first_last_block = first_ip.get_block(4)
    second_last_block = second_ip.get_block(4)

    range_ips = [ip for ip in range(first_last_block, second_last_block + 1)]

    # validating if the ip in the range
    if int(self.ipAddress.split('.')[3]) in range_ips:
      return True

    return False

  def get_list_ips(self, file) -> bool:
    """
    Return the list of ips
    in the file passed for parameter.
    """

    try:
      with open(file, 'r') as f:
        lines = f.readlines()

      return lines

    except:
      print('Some error at read the file.')

  def validate_client_for_list(self, ip_list:list) -> bool:
    """
    Return True if the ip of the client, is in
    the list of ip allows.
    """

    ip_list = [ip.strip('\n') for ip in ip_list] # getting the lines without the end space
    print(self.ipAddress)
    if self.ipAddress in ip_list: # validating the ip
      return True

    return False


  def __str__(self) -> str:
      return f'This is a client with ip {self.ipAddress}'