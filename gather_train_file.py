import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="src input file",
    default="localization-xml-mt/data/enzh/enzh_en_train.json"
)
parser.add_argument(
    "--trg_file", type=str, nargs="*", help="trg input file",
    default=None,
)
parser.add_argument(
    "--output_src_file", type=str, help="src output file",
    default="data/xml/train.en"
)
parser.add_argument(
    "--output_trg_file", type=str, help="trg output file",
    default="data/xml/train.zh")
args = parser.parse_args()

with open(args.src_file, "r", encoding="utf-8") as f:
    src_json = json.load(f)
src_lines = []
for id in src_json["text"]:
    src_lines.append(src_json["text"][id])

with open(args.output_src_file, "w", encoding="utf-8") as f:
    for line in src_lines:
        f.write("%s\n" % line)

if args.trg_file:
    with open(args.trg_file[0], "r", encoding="utf-8") as f:
        trg_json = json.load(f)
    trg_lines = []
    for id in trg_json["text"]:
        trg_lines.append(trg_json["text"][id])

    with open(args.output_trg_file, "w", encoding="utf-8") as f:
        for line in trg_lines:
            f.write("%s\n" % line)
