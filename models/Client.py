"""
This module have the class Client
for model a client of the server.
"""

import sys
sys.path.append('.')

from settings.ips_allows import IP_ALLOWS

class Client:
  """
  Create a client with a ip address.
  """

  def __init__(self, ipAddress) -> None:
      # initial value
      self.ipAddress = ipAddress

  def validate_client(self) -> bool:
    """
    Return True if the ip
    of the client created is in the range
    of the ips allows.
    """

    ip_one = ''
    ip_two = ''
    ranges_ips = []

    import re

    first_ip = IP_ALLOWS[0]
    ip_search = re.search('$', first_ip)

    for c in IP_ALLOWS[1]:
      if c != '.':
        ip_two += c

    return ip_search.group(0)

    # for ip in (range(int(ip_one), int(ip_two))):
    #   ranges_ips.append(str(ip))


    # if self.ipAddress in ranges_ips:
    #   return True

    # return False


  def __str__(self) -> str:
      return f'This is a client with ip {self.ipAddress}'