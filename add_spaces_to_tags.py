import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input", type=str, help="input file",
)
parser.add_argument(
    "--output", type=str, help="output file",
)
args = parser.parse_args()

with open(args.input, "r") as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]

pattern = re.compile(r"</?\w*>")
with open(args.output, "w") as f:
    for line in lines:
        tokens = line.split(" ")
        new_tokens = []
        for token in tokens:
            r = pattern.search(token)
            if not r:
                new_tokens.append(token)
                continue
            last = 0
            while r:
                if r.start() > last:
                    new_tokens.append(token[last: r.start()])
                new_tokens.append(r.group(0))
                last = r.end()
                r = pattern.search(token, last)
            if last < len(token):
                new_tokens.append(token[last:])
        f.write(" ".join(new_tokens) + "\n")
