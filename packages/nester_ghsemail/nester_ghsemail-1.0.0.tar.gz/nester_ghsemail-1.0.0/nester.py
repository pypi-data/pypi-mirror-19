def print_lol(the_list,indent = False,level = 0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(the_list,indent,level+1)
        else:
            if(indent == True):
                for tab_step in range(level):
                    print("\t")
            print(each_item)