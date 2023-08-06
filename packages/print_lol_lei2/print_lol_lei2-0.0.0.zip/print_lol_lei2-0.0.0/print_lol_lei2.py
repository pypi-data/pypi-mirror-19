"""this is the standard way to include a multiple-line comment in your code."""

def print_lol_lei2(the_list,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol_lei2(each_item,level+1)
        else:
            for tab_stop in range(level):
                 print("\t"),
        print(each_item)