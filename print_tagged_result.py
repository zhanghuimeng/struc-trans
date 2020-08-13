import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="src input file",
    default="nist02.tagged.zh"
)
parser.add_argument(
    "--trg_file", type=str, help="trg input file",
    default="nist02.tagged.en"
)
parser.add_argument(
    "--trans_file", nargs="?", help="translation file"
)
parser.add_argument(
    "--output_file", type=str, help="output file",
    default="merged.tagged.txt"
)
args = parser.parse_args()

with open(args.src_file, "r") as f:
    src_lines = f.readlines()
    src_lines = [line.rstrip() for line in src_lines]

with open(args.trg_file, "r") as f:
    trg_lines = f.readlines()
    trg_lines = [line.rstrip() for line in trg_lines]

if args.trans_file:
    with open(args.trans_file, "r") as f:
        trans_lines = f.readlines()
        trans_lines = [line.rstrip() for line in trans_lines]

with open(args.output_file, "w") as f:
    for i in range(len(src_lines)):
        f.write("(%d)\n" % i)
        f.write("%s\n" % src_lines[i])
        f.write("%s\n" % trg_lines[i])
        if args.trans_file:
            f.write("%s\n" % trans_lines[i])
        f.write("\n")
