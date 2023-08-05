def print_list(list_item, indent = False, level = 0, output = sys.stdout):
    for item in list_item:
        if (isinstance(item, list)):
            print_list(item, indent, level + 1, output)
        else:
            if indent:
                for num in range(level):
                    print("\t", end='', file = output)
            print(item, file = output)
