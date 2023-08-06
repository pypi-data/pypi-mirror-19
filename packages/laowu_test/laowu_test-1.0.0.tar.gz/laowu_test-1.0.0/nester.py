"""
    this is the standard way to include a multiple-line comment
    in your code.
"""
def print_fun(the_list,indent=False,level=0):
    for s in the_list:
        if isinstance(s,list):
            print_fun(s,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(s)

