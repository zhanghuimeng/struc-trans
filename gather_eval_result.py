import os
import re
import argparse
import csv
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dir", type=str, help="input directory",
)
parser.add_argument(
    "--limit", type=int, help="number of files to gather",
    default=1000,
)
parser.add_argument(
    "--step", type=int, help="step of eval",
    default=1000,
)
parser.add_argument(
    "--output_pic", type=str, help="output image file",
    default="bleu.png"
)
parser.add_argument(
    "--output_csv", type=str, help="output csv file",
    default="bleu.csv")
args = parser.parse_args()

multi_BLEU = []
pattern = re.compile(r"BLEU = (\d+\.\d+)")
for i in range(1000, args.limit + 1, args.step):
    with open(os.path.join(args.dir, "dev.%d.evalResult" % i), "r") as f:
        content = "".join(f.readlines())
        m = pattern.search(content)
        multi_BLEU.append(float(m.group(1)))
print("MULTI BLEU")
print(str(multi_BLEU))
print()

pattern_bleu = re.compile(r"BLEU: (\d+\.\d+)")
pattern_bleu_xml = re.compile(r"XML BLEU: (\d+\.\d+)")
max_BLEU = -1
max_idx = -1
BLEU = []
BLEU_xml = []
for i in range(1000, args.limit + 1, args.step):
    with open(os.path.join(args.dir, "dev.%d.officialResult" % i), "r") as f:
        content = "".join(f.readlines())
        m = pattern_bleu.search(content)
        BLEU.append(float(m.group(1)))
        if BLEU[-1] > max_BLEU:
            max_BLEU = BLEU[-1]
            max_idx = i
        m = pattern_bleu_xml.search(content)
        BLEU_xml.append(float(m.group(1)))

print("BLEU (paper)")
print(str(BLEU))
print()

print("BLEU (paper_xml)")
print(str(BLEU_xml))
print()

print("Max BLEU: %f" % max_BLEU)
print("Max index: %d" % max_idx)

# l1 = plt.plot(multi_BLEU, label="multi-BLEU")
# l2 = plt.plot(BLEU, label="BLEU(w/ tag)")
# l3 = plt.plot(BLEU_xml, label="BLEU(w tag)")
# plt.legend(handles=[l1, l2, l3])
# plt.savefig(args.output_pic)

with open(args.output_csv, mode="w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["multi-BLEU", "BLEU-w/-tag", "BLEU-w-tag"])
    for i in range(len(multi_BLEU)):
        writer.writerow([multi_BLEU[i], BLEU[i], BLEU_xml[i]])
