import argparse
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from thumt.data.vocab import load_tagged_vocabulary

plt.rcParams['font.sans-serif'] = ['Droid Sans Fallback'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号


def word2idx(seq, vocab):
    id_list = []
    for token in seq:
        if token == "<bos>":
            id_list.append(vocab["word2idx"]["<eos>"])
        elif token in vocab["word2idx"]:
            id_list.append(vocab["word2idx"][token])
        else:
            id_list.append(vocab["word2idx"]["<unk>"])
    return id_list


def gen_typed_matrix(seq_q, seq_k, vocab_q, vocab_k):
    nq = len(seq_q)
    nk = len(seq_k)
    nearest_q = [-1 for _ in range(nq)]
    stack = []

    for i in range(nq):
        x = seq_q[i]
        if vocab_q["tag_type"][x] == -1:
            stack.append(vocab_q["tag_content"][x])
        if len(stack) == 0:
            nearest_q[i] = -1
        else:
            nearest_q[i] = stack[-1]
        if vocab_q["tag_type"][x] == 1 and len(stack) > 0:
            stack.pop()

    typed_matrix = np.zeros([nq, nk], dtype=np.int)
    stack = []
    for j in range(nk):
        x = seq_k[j]
        if vocab_k["tag_type"][x] == -1:
            stack.append(vocab_k["tag_content"][x])
        for i in range(nq):
            # 0: std, 1: in, 2: out
            if nearest_q[i] == -1:
                typed_matrix[i][j] = 0
            elif nearest_q[i] in stack:
                typed_matrix[i][j] = 1
            else:
                typed_matrix[i][j] = 2
        if vocab_k["tag_type"][x] == 1 and len(stack) > 0:
            stack.pop()

    return typed_matrix


# 0: green, 1: red, 2: blue
colors = ["green", "red", "blue"]
cmap = ListedColormap(colors)

def save_attn_fig(filename, seq_q, seq_k, mat, mat_gold):
    nq = len(seq_q)
    nk = len(seq_k)
    extent = (0, nk, nq, 0)
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=((nk + 3) // 4 * 2, (nq + 3) // 4))

    def showfig(ax, title, mat):
        ax.title.set_text(title)
        ax.imshow(mat, vmin=0, vmax=len(cmap.colors), cmap=cmap, extent=extent)
        ax.set_frame_on(False)
        locs = np.arange(nk)
        ax.xaxis.set_ticks(locs, minor=True)
        ax.xaxis.set(ticks=locs + 0.5, ticklabels=seq_k)
        locs = np.arange(nq)
        ax.yaxis.set_ticks(locs, minor=True)
        ax.yaxis.set(ticks=locs + 0.5, ticklabels=seq_q)
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)
        ax.grid(color='w', linewidth=1, which="minor")

    showfig(ax1, "pred", mat)
    showfig(ax2, "gold", mat_gold)

    plt.savefig(filename)
    plt.close()


parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_vocab", type=str, help="src vocabulary",
    required=True
)
parser.add_argument(
    "--tgt_vocab", type=str, help="tgt vocabulary",
    required=True
)
parser.add_argument(
    "--mat_file", type=str, help="attn mat file",
    required=True,
)
parser.add_argument(
    "--output_dir", type=str, help="output dir",
    required=True,
)
args = parser.parse_args()

src_vocab, tgt_vocab = load_tagged_vocabulary([args.src_vocab, args.tgt_vocab])
with open(args.mat_file, "rb") as f:
    attn = pickle.load(f)

n = len(attn["src"])
print("Loaded %d pairs of sentences" % n)
os.makedirs(args.output_dir)

for i in range(n):
    src = attn["src"][i]
    tgt = attn["tgt"][i]
    src_id = word2idx(src, src_vocab)
    tgt_id = word2idx(tgt, tgt_vocab)
    dec_self_attn = attn["dec_self_attn"][i]
    enc_dec_attn = attn["enc_dec_attn"][i]
    dec_self_attn_gold = gen_typed_matrix(
        seq_q=tgt_id, seq_k=tgt_id, vocab_q=tgt_vocab, vocab_k=tgt_vocab
    )
    enc_dec_attn_gold = gen_typed_matrix(
        seq_q=tgt_id, seq_k=src_id, vocab_q=tgt_vocab, vocab_k=src_vocab
    )

    if not (dec_self_attn_gold == dec_self_attn).all():
        save_attn_fig(
            filename=os.path.join(args.output_dir, "%04d_dec_self_attn.png" % i),
            seq_q=tgt,
            seq_k=tgt,
            mat=dec_self_attn,
            mat_gold=dec_self_attn_gold
        )
        print("Checking %d pair dec_self_attn failed" % i)
    if not (enc_dec_attn_gold == enc_dec_attn).all():
        save_attn_fig(
            filename=os.path.join(args.output_dir, "%04d_enc_dec_attn.png" % i),
            seq_q=tgt,
            seq_k=src,
            mat=enc_dec_attn,
            mat_gold=enc_dec_attn_gold
        )
        print("Checking %d pair enc_dec_attn failed" % i)
