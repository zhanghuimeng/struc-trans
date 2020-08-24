import nltk
import pkuseg
import argparse

def segtag(line):
    parts = [""]
    intag = False
    for w in line:
        if w == "<":
            intag = True
            parts.append(w)
        elif w == ">":
            intag = False
            if len(parts) == 0: parts.append("")
            parts[-1] += w
            parts.append("")
        else:
            parts[-1] += w
    return parts


parser = argparse.ArgumentParser()
parser.add_argument(
    "--zh_file", type=str, help="left input file", default="data/news-commentary-v15.zh"
)
parser.add_argument(
    "--en_file", type=str, help="right input file", default="data/news-commentary-v15.en"
)

args = parser.parse_args()

seg = pkuseg.pkuseg()           # 以默认配置加载模型

with open(args.zh_file, "r") as f:
    lines = f.readlines()

with open(args.zh_file + ".tok", "w") as f:
    for line in lines:
        parts = segtag(line.rstrip())
        tokens = []
        for part in parts:
            if len(part) > 0 and part[0] == "<" and part[-1] == ">":
                tokens.append(part)
            else:
                tokens += seg.cut(part)
        f.write("%s\n" % " ".join(tokens))

with open(args.en_file, "r") as f:
    lines = f.readlines()

with open(args.en_file + ".tok", "w") as f:
    for line in lines:
        parts = segtag(line.rstrip())
        tokens = []
        for part in parts:
            if len(part) > 0 and part[0] == "<" and part[-1] == ">":
                tokens.append(part)
            else:
                tokens += seg.cut(part)
        f.write("%s\n" % " ".join(tokens))
