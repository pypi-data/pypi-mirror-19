def print_lol(the_list, intent=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, intent, level+1)
        else:
            if intent:
                for tab_stop in range(level):
                    print '\t',
            print(each_item)
            

