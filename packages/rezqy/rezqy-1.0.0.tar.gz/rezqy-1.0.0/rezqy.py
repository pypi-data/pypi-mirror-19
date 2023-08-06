"""written by zqy
@2017.1.15
"""
def print_lol(the_list):
  """This function is used for
  printing list
  """
  for each_item in the_list:
    if isinstance(each_item,list):
      print_lol(each_item)
    else:
      print(each_item)
