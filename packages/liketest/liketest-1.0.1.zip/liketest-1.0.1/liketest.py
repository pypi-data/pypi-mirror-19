"""这是‘like.py'模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表
，其中可能包含嵌套列表。"""
def print_lol(the_list):
        """这个函数去一个位置，名为'the_list'，这可以是任何python列表。所制定的
        列表中的每个数据项（递归地）输出到屏幕上，各数据项各占一行"""
    for each_item in the_list:
	if isinstance(each_item,list):
	    print_lol(each_item)
	else:
            print(each_item)

			

