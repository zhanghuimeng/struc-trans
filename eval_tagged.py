import argparse


def calc_lcs(a, b):
    n = len(a)
    m = len(b)
    f = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i > 0:
                f[i][j] = max(f[i][j], f[i-1][j])
            if j > 0:
                f[i][j] = max(f[i][j], f[i][j-1])
            if a[i] == b[j]:
                if i > 0 and j > 0:
                    f[i][j] = max(f[i][j], f[i-1][j-1] + 1)
                else:
                    f[i][j] = max(f[i][j], 1)
    if n == 0 or m == 0:
        return 0
    else:
        return f[n-1][m-1]


parser = argparse.ArgumentParser()
parser.add_argument(
    "--evl_file", type=str, help="src input file",
    default="data/UN-zh-en/tagged/test.tagged.en"
)
parser.add_argument(
    "--org_file", type=str, help="trg input file",
    default="data/UN-zh-en/tagged/test.tagged.trans.norm"
)

args = parser.parse_args()

with open(args.evl_file, "r") as f:
    evl_lines = f.readlines()
    evl_lines = [line.rstrip().split(" ") for line in evl_lines]

with open(args.org_file, "r") as f:
    org_lines = f.readlines()
    org_lines = [line.rstrip().split(" ") for line in org_lines]

l = len(evl_lines)

evl_tag_cnt = 0
evl_matched_tot = 0
lcs_length = 0
matched_same_cnt = 0

for i in range(l):
    org_list = []
    evl_list = []
    # calculate list
    for token in org_lines[i]:
        if token.startswith("<") and token.endswith(">"):
            if "/" in token:
                org_list.append((token, "end", token[2:-1]))
            else:
                org_list.append((token, "start", token[1:-1]))
    for token in evl_lines[i]:
        if token.startswith("<") and token.endswith(">"):
            if "/" in token:
                evl_list.append((token, "end", token[2:-1]))
            else:
                evl_list.append((token, "start", token[1:-1]))
    # print(str(org_list))
    # print(str(evl_list))

    # calculate stack for evl_list
    evl_matched_cnt = 0
    stk = []
    evl_tag_cnt += len(evl_list)
    for tup in evl_list:
        if tup[1] == "start":
            stk.append(tup[2])
        else:
            if len(stk) > 0 and stk[-1] == tup[2]:
                stk.pop()
                evl_matched_tot += 2
                evl_matched_cnt += 1

    # calculate stack for org_list
    org_matched_cnt = 0
    stk = []
    for tup in org_list:
        if tup[1] == "start":
            stk.append(tup[2])
        else:
            if len(stk) > 0 and stk[-1] == tup[2]:
                stk.pop()
                org_matched_cnt += 1

    if org_matched_cnt == evl_matched_cnt:
        matched_same_cnt += 1

    # calculate lcs
    a = [tup[2] for tup in org_list]
    b = [tup[2] for tup in evl_list]
    lcs_length += calc_lcs(a, b)


print("Translation matched percent: %f" % (evl_matched_tot / evl_tag_cnt * 100))
print("Similarity: %f" % (lcs_length / evl_tag_cnt * 100))
print("Matched same percent: %f" % (matched_same_cnt / l * 100))
