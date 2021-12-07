"""
This file have the class File
for use.

"""

class File:
  """
  Create a file with a name and path properties.
  """

  def __init__(self, id, path):
    # initials values
    self.id = id
    self.path = path

  def __str__(self) -> str:
    return f'This is a file with id {self.id} and path {self.path}'