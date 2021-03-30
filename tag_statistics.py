import argparse
import re
import nltk
import statistics

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_file", type=str, help="input file",
)
args = parser.parse_args()

with open(args.input_file, "r") as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

pattern = re.compile(r"<(/)?(\w*)>")

tag_enclosing_len_dict = {}
tag_cnt_dict = {}
tag_cnt_all = 0  # all tags cnt
token_cnt_all = 0  # all tags cnt
for line in lines:
    tokens = []
    last = 0
    r = pattern.search(line)
    while r:
        if r.start() > last:
            tokens += nltk.word_tokenize(line[last: r.start() - 1])
        tokens.append(r.group(0))
        last = r.end()
        r = pattern.search(line, last)
    if last < len(line) - 1:
        tokens += nltk.word_tokenize(line[last:])
    token_cnt_all += len(tokens)

    # print(line)
    # print(tokens)

    tag_idx_dict = {}
    for i, token in enumerate(tokens):
        r = pattern.match(token)
        if r:
            content = r.group(2)
            tag_cnt_all += 1
            tag_cnt_dict[content] = tag_cnt_dict.get(content, 0) + 1
            start = True
            if r.group(1) == "/":
                start = False
            if start:
                tag_idx_dict[content] = i
            else:
                if content in tag_enclosing_len_dict:
                    tag_enclosing_len_dict[content].append(i - tag_idx_dict[content] - 1)
                else:
                    tag_enclosing_len_dict[content] = [i - tag_idx_dict[content] - 1]

print("Token cnt: %d" % token_cnt_all)
print("Tag cnt (pair): %d" % (tag_cnt_all // 2))
print("Tag pairs / non_tags: %.02f%%" % (tag_cnt_all // 2 / (token_cnt_all - tag_cnt_all) * 100))
for k, v in tag_cnt_dict.items():
    print("%12s %7d (%6.02f%% enclosing len=%.02f)" % (k, v, v / tag_cnt_all * 100,
                                                       statistics.mean(tag_enclosing_len_dict[k])))
