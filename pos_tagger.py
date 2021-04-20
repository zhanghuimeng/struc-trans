import argparse
import spacy
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--lang", type=str, help="input corpus file",
)
parser.add_argument(
    "--input_file", type=str, help="config file",
)
args = parser.parse_args()

with open(args.input_file, "r") as f:
    lines = f.readlines()

tag_pattern = re.compile(r"</?\w+>")
for line in lines:
    tokens = line.strip().split()
    if args.lang == "en":
        nlp = spacy.load("en_core_web_sm")
    elif args.lang == "zh":
        nlp = spacy.load("zh_core_web_sm")
    # rip off the tags
    new_tokens = []
    for token in tokens:
        if not tag_pattern.match(token):
            new_tokens.append(token)

    doc = nlp(" ".join(new_tokens))
    print(line.strip())
    for token in doc:
        print(token.text, end=" ")
    print()
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk[0].i)
    input()
