import nltk
import pkuseg

seg = pkuseg.pkuseg()           # 以默认配置加载模型

with open("data/news-commentary-v15.zh", "r") as f:
    lines = f.readlines()

with open("data/news-commentary-v15.zh.tok", "w") as f:
    for line in lines:
        tokens = seg.cut(line.rstrip())
        f.write("%s\n" % " ".join(tokens))

with open("data/news-commentary-v15.en", "r") as f:
    lines = f.readlines()

with open("data/news-commentary-v15.en.tok", "w") as f:
    for line in lines:
        tokens = nltk.word_tokenize(line.rstrip())
        f.write("%s\n" % " ".join(tokens))
