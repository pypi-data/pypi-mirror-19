"""
This Module contains inportant function
used with Lists
"""
def Print_lol(ItList , level = 0):
     """ This funtion takes a List Argument and splits it into member items even though
     it is nested with List within List """
     for Ms in ItList:
          if isinstance(Ms , list):
               Print_lol(Ms , level + 1)
          else:
               for tab_stops in range(level):
                    print ("\t" , end = '')
               print (Ms)

