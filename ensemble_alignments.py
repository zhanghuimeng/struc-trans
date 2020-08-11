import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--alignments", type=str, nargs='*', help="Alignment files to ensemble",
)
parser.add_argument(
    "--output", type=str, help="output file",
)

args = parser.parse_args()

alignment_files = args.alignments
n = len(alignment_files)
all_alignments = []
for file in alignment_files:
    with open(file, "r") as f:
        lines = f.readlines()
        lines = [line.rstrip().split(" ") for line in lines]
        alignments = []
        for line in lines:
            alignments.append([])
            for a in line:
                b = a.split("-")
                try:
                    alignments[-1].append((int(b[0]), int(b[1])))
                except:
                    print(a)
    all_alignments.append(alignments)

m = len(all_alignments[0])
with open(args.output, "w") as f:
    for i in range(m):
        cnt_dict = {}
        for j in range(n):
            for a in all_alignments[j][i]:
                cnt_dict[a] = cnt_dict.get(a, 0) + 1
        for a in cnt_dict:
            if cnt_dict[a] >= n:
                f.write("%d-%d " % (a[0], a[1]))
        f.write("\n")
