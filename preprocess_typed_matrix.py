import argparse
import re
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号


def get_matrix(seq_q, seq_k, debug=False):
    nearest_q = []
    stack = []
    nq = len(seq_q)
    nk = len(seq_k)

    tag_prog = re.compile(r"<(/)?(\w*)>")
    for i in range(nq):
        match_obj = tag_prog.match(seq_q[i])
        if match_obj and match_obj.group(1) != "/":
            stack.append(match_obj.group(2))
        if len(stack) == 0:
            nearest_q.append("")
        else:
            nearest_q.append(stack[-1])
        if match_obj and match_obj.group(1) == "/" and len(stack) > 0:
            stack.pop()

    type_matrix = np.zeros([nq, nk])
    stack.clear()
    for j in range(nk):
        match_obj = tag_prog.match(seq_k[j])
        if match_obj and match_obj.group(1) != "/":
            stack.append(match_obj.group(2))
        for i in range(nq):
            # 0: std, 1: in, 2: out
            if nearest_q[i] == "":
                type_matrix[i][j] = 0
            elif nearest_q[i] in stack:
                type_matrix[i][j] = 1
            else:
                type_matrix[i][j] = 2
        if match_obj and match_obj.group(1) == "/" and len(stack) > 0:
            stack.pop()

    if debug:
        extent = (0, nk, nq, 0)
        # plt.imshow(type_matrix, vmin=0, vmax=len(cmap.colors), cmap=cmap, extent=extent)
        _, ax = plt.subplots()
        ax.imshow(type_matrix, vmin=0, vmax=len(cmap.colors), cmap=cmap, extent=extent)
        ax.set_frame_on(False)
        # ax.set_yticks(range(nq))
        # ax.set_yticklabels(seq_q)
        # ax.set_xticks(range(nk))
        # ax.set_xticklabels(seq_k)
        locs = np.arange(nk)
        ax.xaxis.set_ticks(locs, minor=True)
        ax.xaxis.set(ticks=locs + 0.5, ticklabels=seq_k)
        locs = np.arange(nq)
        ax.yaxis.set_ticks(locs, minor=True)
        ax.yaxis.set(ticks=locs + 0.5, ticklabels=seq_q)
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)
        ax.grid(color='w', linewidth=1, which="minor")
        plt.show()

    return type_matrix


parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="source input file",
    default="data/xml/dedup/train.32k.en.dedup.shuf"
)
parser.add_argument(
    "--tgt_file", type=str, help="target input file",
    default="data/xml/dedup/train.32k.zh.dedup.shuf"
)
parser.add_argument(
    "--debug", help="show type matrix", action="store_true")
parser.add_argument(
    "--output_file", type=str, help="output pickle file",
    default="data/xml/dedup/train_att_mat.32k.dedup.shuf.pickle")
args = parser.parse_args()

with open(args.src_file, "r", encoding="UTF-8") as f:
    src_lines = f.readlines()
src_lines = [line.rstrip().split(" ") for line in src_lines]

if args.tgt_file:
    with open(args.tgt_file, "r", encoding="UTF-8") as f:
        tgt_lines = f.readlines()
    tgt_lines = [line.rstrip().split(" ") for line in tgt_lines]
    assert len(src_lines) == len(tgt_lines)

# 0: green, 1: red, 2: blue
colors = ["green", "red", "blue"]
cmap = ListedColormap(colors)

enc_self_matrices = []
for i in range(len(src_lines)):
    enc_self_matrices.append(get_matrix(src_lines[i], src_lines[i], args.debug))

if args.tgt_file:
    dec_self_matrices = []
    enc_dec_matrices = []
    for i in range(len(src_lines)):
        dec_self_matrices.append(get_matrix(tgt_lines[i], tgt_lines[i], args.debug))
        enc_dec_matrices.append(get_matrix(tgt_lines[i], src_lines[i], args.debug))

with open(args.output_file, "wb") as f:
    if args.tgt_file:
        pickle.dump({
            "enc_self_attn": enc_self_matrices,
            "dec_self_attn": dec_self_matrices,
            "enc_dec_attn": enc_dec_matrices,
        }, f)
    else:
        pickle.dump({
            "enc_self_attn": enc_self_matrices,
        }, f)
