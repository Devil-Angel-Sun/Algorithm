import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo', default=42)
args = parser.parse_args(['--foo', '2'])