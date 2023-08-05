def print_list(list_item, indent=False, level = 0):
    for item in list_item:
        if (isinstance(item, list)):
            print_list(item, indent, level + 1)
        else:
            if indent:
                for num in range(level):
                    print("\t", end='')
            print(item)

