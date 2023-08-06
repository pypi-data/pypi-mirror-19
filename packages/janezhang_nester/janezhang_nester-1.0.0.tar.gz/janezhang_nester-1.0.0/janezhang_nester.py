def print_lol(y):
    for i in y:
        if isinstance(i,list):
            print_lol(i)
        else:
            print(i)