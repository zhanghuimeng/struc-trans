import numpy as np
import thumt.data.vocab as vocab
import thumt.utils.helper as helper

src_vocab, tgt_vocab = vocab.load_tagged_vocabulary(
    ["data/example.src.vocab", "data/example.tgt.vocab"])

src_sent_list = ["x", "x", "<a2>", "x", "x", "x", "x", "<i>", "x", "x", "x", "x", "</i>", "</a2>", "x", "<a1>", "x", "x", "</a1>", "x"]
tgt_sent_list = ["x", "x", "x", "<a1>", "x", "</a1>", "<a2>", "x", "<i>", "x", "x", "</i>", "x", "x", "</a2>", "x"]

src_sent_list = [src_vocab["word2idx"][token] for token in src_sent_list]
tgt_sent_list = [tgt_vocab["word2idx"][token] for token in tgt_sent_list]

src_sent = np.array(src_sent_list)
tgt_sent = np.array(tgt_sent_list)
src_sent = np.reshape(src_sent, (1, -1))
tgt_sent = np.reshape(tgt_sent, (1, -1))

tensor = helper.gen_typed_matrix_cpu(src_sent, tgt_sent,
                                     src_vocab, tgt_vocab)
tensor = tensor.cpu().numpy()
tensor = tensor.squeeze()
tensor = tensor[0] * 1 + tensor[1] * 2 + tensor[2] * 3
print(tensor)
