"""这里是我第一个python学习函数"""
def print_lol(the_list):

    """学习函数"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)

        else:
            print(each_item)
