import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="src input file",
    default="data/news-zh-en/tagged/train.zh"
)
parser.add_argument(
    "--trg_file", type=str, help="trg input file",
    default="data/news-zh-en/tagged/train.en"
)
parser.add_argument(
    "--align_file", type=str, help="alignment file",
    default="data/news-zh-en/tagged/gizapp/final_alignment.out"
)
parser.add_argument(
    "--output_file", type=str, help="alignment file",
    default="data/news-zh-en/tagged/gizapp/alignment.view"
)

args = parser.parse_args()

with open(args.src_file, "r") as f:
    src_lines = f.readlines()
    src_lines = [line.rstrip().split(" ") for line in src_lines]

with open(args.trg_file, "r") as f:
    trg_lines = f.readlines()
    trg_lines = [line.rstrip().split(" ") for line in trg_lines]

with open(args.align_file, "r") as f:
    align = f.readlines()
    align = [line.rstrip() for line in align]

with open(args.output_file, "w") as f:
    for i in range(len(src_lines)):
        f.write("#%d\n" % i)
        for j in range(len(src_lines[i])):
            f.write("%s(%d) " % (src_lines[i][j], j))
        f.write("\n")
        for j in range(len(trg_lines[i])):
            f.write("%s(%d) " % (trg_lines[i][j], j))
        f.write("\n")
        f.write("%s\n" % align[i])
        f.write("\n")
