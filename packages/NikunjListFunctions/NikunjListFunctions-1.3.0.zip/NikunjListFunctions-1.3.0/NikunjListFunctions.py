"""
This Module contains inportant function
used with Lists
"""
def Print_lol(ItList , indent = False , level = 0):
     """ This funtion takes a List Argument and splits it into member items even though
     it is nested with List within List.
     The second Argument gives the level of Tab indetation required
     """
     for Ms in ItList:
          if isinstance(Ms , list):
               Print_lol(Ms , indent , level + 1)
          else:
               if indent:
                    for tab_stops in range(level):
                         print ("\t" , end = '')
               print (Ms)

