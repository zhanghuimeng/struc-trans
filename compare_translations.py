import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="source file",
)
parser.add_argument(
    "--trans_files", type=str, nargs="+", help="translation files"
)
parser.add_argument(
    "--ref_file", type=str, help="reference file"
)
parser.add_argument(
    "--output", type=str, help="output file"
)

args = parser.parse_args()

if args.src_file:
    with open(args.src_file, "r") as f:
        src_lines = f.readlines()
        src_lines = [line.rstrip() for line in src_lines]
else:
    src_lines = None
if args.ref_file:
    with open(args.ref_file, "r") as f:
        ref_lines = f.readlines()
        ref_lines = [line.rstrip() for line in ref_lines]
else:
    ref_lines = None
trans_files = []
for file in args.trans_files:
    with open(file, "r") as f:
        trans_lines = f.readlines()
        trans_lines = [line.rstrip() for line in trans_lines]
    trans_files.append(trans_lines)

n = len(trans_files[0])
with open(args.output, "w") as f:
    for i in range(n):
        f.write("(%d)\n" % i)
        if src_lines:
            f.write("src: %s\n" % src_lines[i])
        if ref_lines:
            f.write("ref: %s\n" % ref_lines[i])
        for j in range(len(trans_files)):
            f.write("trans %d: %s\n" % (j, trans_files[j][i]))
        f.write("\n")
