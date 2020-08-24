import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--json_file", type=str, help="json id file",
    default="localization-xml-mt/data/enzh/enzh_zh_dev.json"
)
parser.add_argument(
    "--input_file", type=str, help="translation output",
    default="exp/xml-baseline/dev.trans.norm"
)
parser.add_argument(
    "--output_file", type=str, help="json output",
    default="exp/xml-baseline/dev.trans.norm.json"
)
parser.add_argument(
    "--remove_space", action="store_true"
)
args = parser.parse_args()

with open(args.json_file, "r") as f:
    src_json = json.load(f)
id_list = []
for id in src_json["text"]:
    id_list.append(id)

with open(args.input_file, "r") as f:
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    if args.remove_space:
        lines = [line.replace(" ", "") for line in lines]

output = {"lang": "zh", "type": "translation", "text": {}}
for i in range(len(id_list)):
    output["text"][id_list[i]] = lines[i]

with open(args.output_file, "w", encoding='utf8') as f:
    json.dump(output, f, ensure_ascii=False)
