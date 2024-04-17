import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--length', default='10', type=int)
parser.add_argument('--width', default=10.5, type=int)
args = parser.parse_args()