"""
This module have some utils functions
for use in the server.
"""

import sys
sys.path.append('.')

from models.File import File

def get_files_paths(config_file) -> list:
  """
  Return a list with each line of
  the file of configuration.
  """

  lines_files = []

  # open for get the lines and return ir
  with open(config_file, 'r') as f:
    lines = f.readlines()

    for line in lines:
      lines_files.append(line.strip('\n'))

  return lines_files


def get_files_object(files:list) -> list:
  """
  Return a list of objects File.
  """

  new_list_files = [] # list for return

  # recorriendo for show it and return
  for indx, file in enumerate(files, start = 0):
    file_current = File(indx, file)
    new_list_files.append(file_current)

  return new_list_files


def validate_config_file(config_file) -> bool:
  """
  Return True if the config file is found.
  """

  # validating the file
  try:
    f = open(config_file, 'r')
    return True

  # in case the file not found
  except FileNotFoundError:
    return False


def get_client(request:str) -> str:
  """
  Return the ip of the client
  that visit the server.
  """

  ip_client = request.headers['host']

  return ip_client