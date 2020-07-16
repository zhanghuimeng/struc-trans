import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--left_file", type=str, help="left input file"
)
parser.add_argument(
    "--right_file", type=str, help="right input file"
)

parser.add_argument(
    "--output", type=str, help="output file"
)

args = parser.parse_args()

with open(args.left_file, "r") as f:
    left_lines = f.readlines()

with open(args.right_file, "r") as f:
    right_lines = f.readlines()

assert len(left_lines) == len(right_lines)

with open(args.output, "w") as f:
    for i in range(len(left_lines)):
        f.write("%s ||| %s\n" % (left_lines[i].rstrip(), right_lines[i].rstrip()))
