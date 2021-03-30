import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_dir", type=str, help="input file",
    default="zh/articles",
)
args = parser.parse_args()