import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="src input file",
    default="data/xml/dedup/train.en.tok"
)
parser.add_argument(
    "--tgt_file", type=str, help="tgt input file",
    default="data/xml/dedup/train.zh.tok"
)
parser.add_argument(
    "--mat_file", type=str, help="attn mat file",
    required=True,
    default="data/xml/dedup/fastalign/train.final.align"
)
parser.add_argument(
    "--output_file", type=str, help="output file",
    default="data/xml/dedup/train.en.dedup"
)
args = parser.parse_args()

src_lines = None
if args.src_file is not None:
    with open(args.src_file, "r") as f:
        src_lines = f.readlines()
    src_lines = [line.rstrip() for line in src_lines]

tgt_lines = None
if args.tgt_file is not None:
    with open(args.tgt_file, "r") as f:
        tgt_lines = f.readlines()
    tgt_lines = [line.rstrip() for line in tgt_lines]

enc_self_attn = None
dec_self_attn = None
enc_dec_attn = None
with open(args.mat_file, "rb") as f:
    attn_mat = pickle.load(f)
if "src" in attn_mat:
    src_lines = attn_mat["src"]
if "tgt" in attn_mat:
    tgt_lines = attn_mat["tgt"]