"""
This file have the class Ip for create
a ip object.
"""

class Ip:
  """
  Create a Ip objcet with a content
  and with the blocks list of the ip.

  Sample of the Model:
  192.153.12.54     [ 192,   153,   12,    54]
                    Block1 Block2 Block3 Block4

  Also the length of the ip created.

  """

  def __init__(self, content:str) -> None:
    self.content = content
    self.len = len(content)

  def get_block(self, block_number:int) -> list:
    """
    Return the list of blocks of
    the ip.

    All the values are int.
    """

    if type(block_number) not in [int]:
      raise TypeError('The number for get the block of the ip must be a int.')

    # getting the values for return
    block_1 = int(self.content.split('.')[0])
    block_2 = int(self.content.split('.')[1])
    block_3 = int(self.content.split('.')[2])
    block_4 = int(self.content.split('.')[3])

    # blocks_list = [block_1, block_2, block_3, block_4]

    # validating for return
    if block_number == 1:
      return block_1
    if block_number == 2:
      return block_2
    if block_number == 3:
      return block_3
    if block_number == 4:
      return block_4

  def __str__(self) -> str:
      return f'This is a ip with a length of {self.len}.'