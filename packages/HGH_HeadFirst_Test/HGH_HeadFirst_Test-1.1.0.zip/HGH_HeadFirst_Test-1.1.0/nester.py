def print_lol(the_list, level):
    '''
    第一个参数是列表
    第二个参数用来在遇到嵌套列表时插入制表符
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level + 1)
        else:
            for tab_stop in range(level):
                print("\t", end = '')#每层缩进显示一个TAB制表符
            print(each_item)
