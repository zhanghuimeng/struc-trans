import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument(
    "--left_file", type=str, help="left input file", default="data/UN-zh-en/tmp.zh.tok"
)
parser.add_argument(
    "--right_file", type=str, help="right input file", default="data/UN-zh-en/tmp.en.tok"
)
parser.add_argument(
    "--align_file", type=str, help="alignment file", default="data/UN-zh-en/tmp.final.align"
)
parser.add_argument(
    "--output_left_file", type=str, help="output file", default="data/UN-zh-en/tmp.tagged.zh"
)
parser.add_argument(
    "--output_right_file", type=str, help="output file", default="data/UN-zh-en/tmp.tagged.en"
)
parser.add_argument(
    "--max_len", type=int, help="Max len of THUMT", default=256
)
args = parser.parse_args()

open_tags = ["<%s>" % chr(i) for i in range(ord('a'), ord('z') + 1)]
close_tags = ["</%s>" % chr(i) for i in range(ord('a'), ord('z') + 1)]

with open(args.left_file, "r", encoding='UTF-8') as f:
    left_lines = f.readlines()
    left_lines = [line.rstrip().split() for line in left_lines]
with open(args.right_file, "r", encoding='UTF-8') as f:
    right_lines = f.readlines()
    right_lines = [line.rstrip().split() for line in right_lines]

tagged_left_lines = []
tagged_right_lines = []

original_exceed_num = 0
processed_exceed_num = 0

with open(args.align_file, "r", encoding='UTF-8') as f:
    cnt = 0  # id of line
    for line in f:
        n = len(left_lines[cnt])
        m = len(right_lines[cnt])
        if n > args.max_len or m > args.max_len:
            original_exceed_num += 1
        left_alignments = [set() for i in range(n)]
        right_alignments = [set() for i in range(m)]
        # Find out the lines
        for s in line.rstrip().split(" "):
            a = s.split("-")
            x, y = int(a[0]), int(a[1])
            left_alignments[x].add(y)
            right_alignments[y].add(x)
        f = []
        for i in range(n):
            for j in range(i, n):
                visited_set = set()
                for k in range(i, j+1):
                    for y in left_alignments[k]:
                        ok = True
                        for x in right_alignments[y]:
                            if x < i or x > j:
                                ok = False
                                break
                        if ok: visited_set.add(y)
                right_visited = list(visited_set)
                right_visited = sorted(right_visited)
                last = 0
                right_consec_list = []
                for k in range(1, len(right_visited)):
                    if not right_visited[k] == right_visited[k - 1] + 1:
                        right_consec_list.append((right_visited[last], right_visited[k - 1]))
                        last = k
                if right_visited:
                    right_consec_list.append((right_visited[last], right_visited[-1]))

                for l, r in right_consec_list:
                    left_visited = [False] * (j - i + 1)
                    for y in range(l, r + 1):
                        for x in right_alignments[y]:
                            left_visited[x - i] = True
                    if all(left_visited):
                        f.append((i, j, l, r))

        # Add tags
            tag_tot = (n + m) // 16
        tag_cnt = 0
        left_visited = [False] * n
        right_visited = [False] * m
        align = []
        # Random select tags
        if f:
            for _ in range(tag_tot * 50):
                if tag_cnt >= tag_tot: break
                i, j, l, r = random.choice(f)
                if all([not x for x in left_visited[i:j+1]]) and all([not x for x in right_visited[l:r+1]]):
                    tag_cnt += 1
                    align.append((i, j, l, r))
                    for k in range(i, j+1): left_visited[k] = True
                    for k in range(l, r+1): right_visited[k] = True
        # Sort tags and mark them
        align = sorted(align)
        left_tags = [""] * (2 * n)
        right_tags = [""] * (2 * m)
        for idx, (i, j, l, r) in enumerate(align):
            left_tags[i * 2] = right_tags[l * 2] = open_tags[idx % len(open_tags)]
            left_tags[j * 2 + 1] = right_tags[r * 2 + 1] = close_tags[idx % len(close_tags)]
        # Add tags to line
        tagged_left_lines.append([])
        for i, token in enumerate(left_lines[cnt]):
            if left_tags[i * 2]:
                tagged_left_lines[-1].append(left_tags[i * 2])
            tagged_left_lines[-1].append(token)
            if left_tags[i * 2 + 1]:
                tagged_left_lines[-1].append(left_tags[i * 2 + 1])
        tagged_right_lines.append([])
        for i, token in enumerate(right_lines[cnt]):
            if right_tags[i * 2]:
                tagged_right_lines[-1].append(right_tags[i * 2])
            tagged_right_lines[-1].append(token)
            if right_tags[i * 2 + 1]:
                tagged_right_lines[-1].append(right_tags[i * 2 + 1])

        cnt += 1

        if len(tagged_left_lines[-1]) > args.max_len or len(tagged_right_lines[-1]) > args.max_len:
            processed_exceed_num += 1
        if cnt % 1000 == 0:
            print("%d/%d" % (cnt, len(left_lines)))
            print("Before: %f" % (original_exceed_num / cnt))
            print("After: %f" % (processed_exceed_num / cnt))

with open(args.output_left_file, "w", encoding='UTF-8') as f:
    for line in tagged_left_lines:
        f.write("%s\n" % (" ".join(line)))

with open(args.output_right_file, "w", encoding='UTF-8') as f:
    for line in tagged_right_lines:
        f.write("%s\n" % (" ".join(line)))
