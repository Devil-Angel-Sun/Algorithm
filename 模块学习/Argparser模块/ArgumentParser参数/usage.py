import argparse
parser = argparse.ArgumentParser(prog = 'Add usage', usage='%(prog)s [options]')
parser.add_argument('--example', help = 'Example help')
parser.add_argument('--example1', nargs='?', help='Example1 help')
parser.add_argument('example2', nargs='+', help='Example2 help')
args = parser.parse_args()