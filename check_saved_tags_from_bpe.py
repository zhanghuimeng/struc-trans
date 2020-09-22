import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--ori_file", type=str, help="original file",
    default="data/xml/dedup/train.en.dedup"
)
parser.add_argument(
    "--pro_file", type=str, help="processed file",
    default="data/xml/dedup/train.32k.en.dedup"
)
args = parser.parse_args()

with open(args.ori_file, "r") as f:
    ori_lines = f.readlines()
    ori_lines = [line.rstrip().split(" ") for line in ori_lines]

with open(args.pro_file, "r") as f:
    pro_lines = f.readlines()
    pro_lines = [line.rstrip().split(" ") for line in pro_lines]

assert len(ori_lines) == len(pro_lines)

prog = re.compile(r"<(/)?(\w*)>")

for i in range(len(pro_lines)):
    ori_tags = []
    for token in ori_lines[i]:
        if prog.match(token):
            ori_tags.append(token)
    pro_tags = []
    for token in pro_lines[i]:
        if prog.match(token):
            pro_tags.append(token)
    if ori_tags != pro_tags:
        print(ori_lines[i])
        print(ori_tags)
        print(pro_lines[i])
        print(pro_tags)
        exit(-1)

print("ok")
