import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--vocabulary", type=str, help="input file",
)
parser.add_argument(
    "--output", type=str, help="output file",
)
args = parser.parse_args()

with open(args.vocabulary, "r") as f:
    lines = f.readlines()
vocabs = [line.strip() for line in lines]

is_word_start = {}
for word in vocabs:
    word_stripped = word.replace("▁", "")
    # 英文例：
    # source: "I saw a girl with a telescope."
    # tokenized: "▁I ▁saw ▁a ▁girl ▁with ▁a ▁te le s c o pe ."
    # 在SPM中，"▁"符号替代了空格，因此在英文中，一般来说，只有由"▁"开头的token才是一个词的开始部分。
    # 但很显然中文并不是这样。
    # TODO: 所以该脚本可能需要根据其他语言对修改，改完后最好手动检查一下结果
    if not word.startswith("▁") and word_stripped.encode().isalpha():
        is_word_start[word] = False
    else:
        is_word_start[word] = True

with open(args.output, "w") as f:
    json.dump(is_word_start, f)
