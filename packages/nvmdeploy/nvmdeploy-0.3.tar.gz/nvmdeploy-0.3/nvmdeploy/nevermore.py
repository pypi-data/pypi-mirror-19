# coding=utf-8
import argparse
import sys
from fastinit import need_init, startInit, reInit, addTask, deleteTask, listTask, doTask

nvm_deploy = """
 \033[1;32;40m (/≧▽≦)/ *** 快速发布 pod的命令行工具 *** ヾ(^▽^ヾ)
 \033[1;33;40m BETA 版本 v0.3 \033[0m
"""

print nvm_deploy

if len(sys.argv) == 1:
    sys.argv.append('--help')

parser = argparse.ArgumentParser()
parser.add_argument('-i','--init',help="快速初始化命令行工具", action="store_true")
parser.add_argument('-a','--add', help="添加新的 task", action="store_true")
parser.add_argument('-d', '--delete', help="删除指定名称的 task")
parser.add_argument('-t', '--task', help="需要发布的 task 名称")
parser.add_argument('-l', '--list', help="查看所有 task", action="store_true")

args = parser.parse_args()

#print args

if __name__ == '__main__':
    try:
        if need_init():
            startInit()
        else:
            if args.task:
                doTask(args.task)
            elif args.add:
                addTask()
            elif args.init:
                reInit()
            elif args.delete:
                deleteTask(args.delete)
            elif args.list:
                listTask()

    except:
        print("\n \033[1;31;40m 异常退出\n")