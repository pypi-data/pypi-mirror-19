# Recursive function
import sys 

def myfunction (cusine, indent = False ,level = 0, fh =sys.stdout):
    for i in cusine:
        if isinstance(i, list):
            myfunction(i, indent ,level + 1, fh)
        else:
            if indent:
                for tabCharacter in range(level):
                    print("\t", end = '', file = fh)
            print(i, file = fh)

#food = ["English","Italian","Indian",["Curry", ["Bindi","Dal","Aloo"]]]

#myfunction(food)
