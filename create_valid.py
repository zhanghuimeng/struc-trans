import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument(
    "--left_file", type=str, help="left input file", default="data/UN-zh-en/UNv1.0.en-zh.zh"
)
parser.add_argument(
    "--right_file", type=str, help="right input file", default="data/UN-zh-en/UNv1.0.en-zh.en"
)
parser.add_argument(
    "--valid_left_file", type=str, help="validation output file", default="data/UN-zh-en/valid.zh"
)
parser.add_argument(
    "--valid_right_file", type=str, help="validation output file", default="data/UN-zh-en/valid.en"
)
parser.add_argument(
    "--test_left_file", type=str, help="test output file", default="data/UN-zh-en/test.zh"
)
parser.add_argument(
    "--test_right_file", type=str, help="test output file", default="data/UN-zh-en/test.en"
)

args = parser.parse_args()

with open(args.left_file, "r") as f:
    left_lines = f.readlines()

with open(args.right_file, "r") as f:
    right_lines = f.readlines()

l = len(left_lines)
indices = list(range(l))
random.shuffle(indices)

valid = []
test = []
for i in indices:
    if i < 1000000:
        continue
    if len(valid) < 3000:
        valid.append(i)
    elif len(test) < 3000:
        test.append(i)
    else:
        break

with open(args.valid_left_file, "w") as f:
    for i in valid:
        f.write(left_lines[i])

with open(args.valid_right_file, "w") as f:
    for i in valid:
        f.write(right_lines[i])

with open(args.test_left_file, "w") as f:
    for i in test:
        f.write(left_lines[i])

with open(args.test_right_file, "w") as f:
    for i in test:
        f.write(right_lines[i])
