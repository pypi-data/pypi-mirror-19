def tsync(time):
    if '-' in time:
        splitter = '-'
    elif ':' in time:
        splitter = ':'
    else:
        return(time)
    (mins, secs) = time.split(splitter)
    return(mins+'.'+secs)
