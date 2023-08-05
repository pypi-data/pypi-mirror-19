def print_list(list_item, level = 0):
    if (isinstance(list_item, list)):
        for item in list_item:
            print_list(item, level + 1)
    else:
        for num in range(level):
            print("\t", end='')
        print(list_item)

