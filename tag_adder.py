import argparse
import collections
import nltk
import yaml
import json
import random
import numpy as np

CLAUSE_PUNCS = {
    "en": "~!,.?:'\"()",
    "zh": "~!,.?:'\"()、！，。？…：“”（）《》「」",
    # TODO: 增加其他语言的分句符号
}

Token = collections.namedtuple("Token", "token type name word_start")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--corpus_file", type=str, help="input corpus file",
)
parser.add_argument(
    "--lang", type=str, help="language of input corpus file",
)
parser.add_argument(
    "--config_file", type=str, help="config file",
)
parser.add_argument(
    "--output_file", type=str, help="output file",
)
parser.add_argument(
    "--is_word_start", type=str, help="word start dict",
)
parser.add_argument(
    "--no_pass_clauses", action="store_true", help="whether to use CLAUSE_PUNCS or not",
)
args = parser.parse_args()

with open(args.config_file, "r") as f:
    my_dict = yaml.load(f, Loader=yaml.FullLoader)
tag_name = []
tag_prob = []
tag_enclosed = []
for k in my_dict["tag_info"]:
    tag_name.append(k)
    tag_prob.append(my_dict["tag_info"][k]["p"])
    tag_enclosed.append(my_dict["tag_info"][k]["len"])
M = len(tag_name)

with open(args.is_word_start, "r") as f:
    is_word_start = json.load(f)

token_cnt_all = 0
tag_cnt = [0] * M
N = 0

# fail statistics
open_close_fail_cnt = 0
whole_mask_fail_cnt = 0
clause_pass_fail_cnt = 0

with open(args.corpus_file, "r") as f:
    with open(args.output_file, "w") as fw:
        for line in f:
            tokens = line.rstrip().split(" ")

            tokens = [Token(token=token, type="plain", name="",
                            word_start=is_word_start.get(token, True)) for token in tokens]
            L = len(tokens)
            token_cnt_all += L

            p0 = my_dict["tag_percent"]
            p1 = 1 / (p0 * L + 1)
            # trial to add tags (using geometry distribution)
            while random.random() > p1:
                # select tag by multinomial distribution
                a = np.random.multinomial(1, tag_prob)
                selected_tag_idx = -1
                for i in range(M):
                    if a[i] != 0:
                        selected_tag_idx = i
                        break

                # try to insert a tag
                all_enclose_trial_cnt = 0
                while all_enclose_trial_cnt < 1000:
                    enclose_len = round(np.random.normal(tag_enclosed[selected_tag_idx]))
                    if enclose_len > len(tokens):
                        enclose_len = len(tokens)
                    one_len_trail_cnt = 0
                    while one_len_trail_cnt < 15:
                        start = random.randint(0, len(tokens) - enclose_len)
                        end = start + enclose_len
                        # whole word masking
                        while start < len(tokens) and not tokens[start].word_start:
                            start += 1
                        while end < len(tokens) and not tokens[end].word_start:
                            end += 1
                        if start >= end or end > len(tokens):
                            whole_mask_fail_cnt += 1
                            one_len_trail_cnt += 1
                            continue
                        # check open/close tags
                        open_close_cnt = 0
                        have_punc = False
                        for i in range(start, end):
                            if tokens[i].type == "start":
                                open_close_cnt += 1
                            elif tokens[i].type == "end":
                                open_close_cnt -= 1
                            if open_close_cnt < 0:
                                open_close_fail_cnt += 1
                                break
                            if args.no_pass_clauses:
                                for punc in CLAUSE_PUNCS[args.lang]:
                                    if punc in tokens[i].token:
                                        have_punc = True
                                        break
                                if have_punc:
                                    clause_pass_fail_cnt += 1
                                    break
                        if open_close_cnt != 0 or have_punc:
                            one_len_trail_cnt += 1
                            continue
                        new_tokens = []
                        if start > 0:
                            new_tokens += tokens[:start]
                        new_tokens.append(
                            Token(token="<%s>" % tag_name[selected_tag_idx], type="start",
                                  name=tag_name[selected_tag_idx], word_start=True))
                        new_tokens += tokens[start: end]
                        new_tokens.append(
                            Token(token="</%s>" % tag_name[selected_tag_idx], type="end",
                                  name=tag_name[selected_tag_idx], word_start=True))
                        if end < len(tokens):
                            new_tokens += tokens[end:]
                        tokens = new_tokens
                        one_len_trail_cnt = -1
                        break
                    if one_len_trail_cnt == -1:
                        tag_cnt[selected_tag_idx] += 1
                        break
                    else:
                        all_enclose_trial_cnt += one_len_trail_cnt

            tokens = [token.token for token in tokens]
            fw.write(" ".join(tokens) + "\n")
            N += 1

            if N % 10000 == 0:
                print("N = %d" % N)
                print("Added tag percentage: %.02f%% (expected: %.02f%%)" % (sum(tag_cnt) / token_cnt_all * 100,
                                                                             my_dict["tag_percent"] * 100))
                for i in range(M):
                    print("Tag <%s> percentage: %.02f%% (expected: %.02f%%)" % (tag_name[i], tag_cnt[i] / sum(tag_cnt) * 100,
                                                                                tag_prob[i] * 100))
                print("Failures:")
                print("Whole mask fails: %d" % whole_mask_fail_cnt)
                print("Open/close tag fails: %d" % open_close_fail_cnt)
                print("Clause fails: %d" % clause_pass_fail_cnt)
