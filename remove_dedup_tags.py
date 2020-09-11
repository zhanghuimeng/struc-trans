import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_file", type=str, help="input deduped tag file",
    default="exp/xml-dedup-baseline/dev.trans.norm"
)
parser.add_argument(
    "--output_file", type=str, help="output tag file",
    default="exp/xml-dedup-baseline/dev.trans.norm.dup"
)
args = parser.parse_args()

with open(args.input_file, "r") as f:
    lines = f.readlines()
    lines = [line.rstrip().split(" ") for line in lines]

with open(args.output_file, "w") as f:
    for line in lines:
        for i in range(len(line)):
            match_obj = re.match(r"<(/)?(\w*)(_\d+)>", line[i])
            if match_obj:
                line[i] = line[i].replace(match_obj.group(2) + match_obj.group(3), match_obj.group(2))
        f.write("%s\n" % " ".join(line))
