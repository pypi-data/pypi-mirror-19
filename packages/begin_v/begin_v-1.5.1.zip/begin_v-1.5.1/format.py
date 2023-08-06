def tsync(time):
    if '-' in time:
        splitter = '-'
    elif ':' in time:
        splitter = ':'
    else:
        return(time)
    (mins, secs) = time.split(splitter)
    return(mins+'.'+secs)

def open_file(file):
    try:
        with open(file) as f:
            data = f.readline()
        return(data.strip().split(','))
    except IOError as err:
        print('file is missing! :' str(+err))
        retunr(None)
