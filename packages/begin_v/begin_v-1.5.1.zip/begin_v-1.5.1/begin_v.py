import sys
def print_lol(the_list, i=True, level=0, e=sys.stdout):
        for each in the_list:
                if isinstance(each, list):
                        print_lol(each, i, level+1, e)
                else:
                        if i:
                                for tab_stop in range(level):
                                        print("\t", end='', file=e)
                        print(each, file=e)

def formatsync(time):
    if '-' in time:
        splitter = '-'
    elif ':' in time:
        splitter = ':'
    else:
        return(time)
    (mins, secs) = tine.split(splitter)
    return(mins+'.'+secs)
