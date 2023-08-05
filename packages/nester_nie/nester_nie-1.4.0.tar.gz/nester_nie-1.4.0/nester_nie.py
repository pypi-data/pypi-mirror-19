#!/usr/local/bin/python3
import sys

def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1,fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end="",file=fh)
            print(each_item,file=fh)

if __name__ == "__main__":
    mylist = ['Hello',["apple","banner",["1","2","3"]],'world']
    print_lol(mylist,True,0)
