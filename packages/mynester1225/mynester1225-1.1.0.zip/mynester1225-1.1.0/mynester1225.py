
def printall(listitem,level):
    print("before sorting",listitem)
    for eachone in listitem:
       if isinstance(eachone,list):
            printall(eachone,level+1)
       else:
           for evtab in range(level):
               print("\t", end='')
           print(eachone)

