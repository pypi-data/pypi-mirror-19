"""
This Module contains inportant function
used with Lists
"""
def Print_lol(ItList):
     """ This funtion takes a List Argument and splits it into member items even though
     it is nested with List within List """
     for Ms in ItList:
          if isinstance(Ms , list):
               Print_lol(Ms)
          else:
               print (Ms)


