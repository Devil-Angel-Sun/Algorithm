# prog参数可以修改ArgumentParser对象的默认文件名
# 不论程序的文件名是来自sys.argv[0]，不是来自参数prog，都可以通过%(prog)s来引用程序的文件名。
import argparse
parser = argparse.ArgumentParser(prog = 'Add prog')
parser.add_argument('--example', help = 'Example of the %(prog)s program')
args = parser.parse_args()