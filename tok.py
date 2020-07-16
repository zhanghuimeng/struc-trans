import nltk
import pkuseg
import argparse

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
        tokens = seg.cut(line.rstrip())
        f.write("%s\n" % " ".join(tokens))

with open(args.en_file, "r") as f:
    lines = f.readlines()

with open(args.en_file + ".tok", "w") as f:
    for line in lines:
        tokens = nltk.word_tokenize(line.rstrip())
        f.write("%s\n" % " ".join(tokens))
