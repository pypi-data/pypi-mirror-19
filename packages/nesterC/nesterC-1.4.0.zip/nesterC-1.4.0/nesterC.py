"""这是"nester.py"模块，提供了一个名为print_lol()的函数用来打印列表，
    其中包含或不包含嵌套列表。"""
import sys
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """这个函数有一个位置参数，名为"the_list"，
    这可以是任何Python列表（包含或不包含嵌套列表），所提供列表中的各个数据项会（递归地）
    打印到屏幕上，而且各占一行。"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(each_item, file=fh)
