def print_list(list_item, level = 0):
    for item in list_item:
        if (isinstance(item, list)):
            print_list(item, level + 1)
        else:
            for num in range(level):
                print("\t", end='')
            print(item)
