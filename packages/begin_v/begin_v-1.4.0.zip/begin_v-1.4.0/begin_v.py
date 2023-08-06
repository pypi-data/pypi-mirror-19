def print_lol(the_list, i=True, level=0, e=sys.stdout):
        for each in the_list:
                if isinstance(each, list):
                        print_lol(each, i, level+1, e)
                else:
                        if i:
                                for tab_stop in range(level):
                                        print("\t", end='', file=e)
                        print(each, file=e)
