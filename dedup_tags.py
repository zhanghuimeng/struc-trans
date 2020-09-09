import argparse
import re
import numpy as np


def get_tag_type_content(seq):
    n = len(seq)
    tag_type = [""] * n
    tag_content = [""] * n
    for i in range(n):
        match_obj = re.match(r"<(/)?(\w*)>", seq[i])
        if match_obj:
            if match_obj.group(1) == "/":
                tag_type[i] = "end"
            else:
                tag_type[i] = "start"
            tag_content[i] = match_obj.group(2)
        else:
            tag_type[i] = "std"
            tag_content[i] = ""
    return tag_type, tag_content


def get_tag_span(seq, tag_type, tag_content):
    n = len(seq)
    stack = []
    tag_span_dict = {}
    for i in range(n):
        if tag_type[i] == "start":
            stack.append((tag_content[i], i))
        elif tag_type[i] == "end":
            _, start = stack[-1]
            stack.pop()
            if tag_content[i] in tag_span_dict:
                tag_span_dict[tag_content[i]].append((start, i))
            else:
                tag_span_dict[tag_content[i]] = [(start, i)]
    return tag_span_dict


parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="src input file",
    default="data/xml/dedup/train.en.tok"
)
parser.add_argument(
    "--trg_file", type=str, help="trg input file",
    default="data/xml/dedup/train.zh.tok"
)
parser.add_argument(
    "--align_file", type=str, help="alignment file",
    default="data/xml/dedup/fastalign/train.final.align"
)
parser.add_argument(
    "--output_src_file", type=str, help="src output file",
    default="data/xml/dedup/train.en.dedup"
)
parser.add_argument(
    "--output_trg_file", type=str, help="trg output file",
    default="data/xml/dedup/train.zh.dedup")
args = parser.parse_args()

with open(args.src_file, "r") as f:
    src_lines = f.readlines()
    src_lines = [line.rstrip().split(" ") for line in src_lines]

with open(args.trg_file, "r") as f:
    trg_lines = f.readlines()
    trg_lines = [line.rstrip().split(" ") for line in trg_lines]

with open(args.align_file, "r") as f:
    align_lines = f.readlines()
    align_lines = [line.rstrip().split(" ") for line in align_lines]

l = len(src_lines)
for i in range(l):
    n = len(src_lines[i])
    m = len(trg_lines[i])
    align_set = [set() for _ in range(n)]
    for a in align_lines[i]:
        a2 = a.split("-")
        align_set[int(a2[0])].add(int(a2[1]))

    tag_type_src, tag_content_src = get_tag_type_content(src_lines[i])
    tag_type_trg, tag_content_trg = get_tag_type_content(trg_lines[i])
    tag_span_dict_src = get_tag_span(src_lines[i], tag_type_src, tag_content_src)
    tag_span_dict_trg = get_tag_span(trg_lines[i], tag_type_trg, tag_content_trg)

    # print(" ".join(src_lines[i]))
    # print(" ".join(trg_lines[i]))
    # print(tag_span_dict_src)
    # print(tag_span_dict_trg)

    # 找到每个tag span对齐到target端的span最多的
    for tag in tag_span_dict_src:
        span_src_list = tag_span_dict_src[tag]
        span_trg_list = tag_span_dict_trg[tag]
        n1 = len(span_src_list)
        for j in range(n1):
            cnt = [0] * n1
            l_src, r_src = span_src_list[j]
            for ts in range(l_src, r_src + 1):
                for tt in align_set[ts]:
                    for k in range(n1):
                        if span_trg_list[k][0] <= tt <= span_trg_list[k][1]:
                            cnt[k] += 1
            align = np.argmax(cnt)
            l_trg, r_trg = span_trg_list[align]
            src_lines[i][l_src] = trg_lines[i][l_trg] = "<%s_%d>" % (tag_content_src[l_src], j)
            src_lines[i][r_src] = trg_lines[i][r_trg] = "</%s_%d>" % (tag_content_src[l_src], j)

    # print(" ".join(src_lines[i]))
    # print(" ".join(trg_lines[i]))
    # input()

with open(args.output_src_file, "w") as f:
    f.writelines([" ".join(line) + "\n" for line in src_lines])

with open(args.output_trg_file, "w") as f:
    f.writelines([" ".join(line) + "\n" for line in trg_lines])
