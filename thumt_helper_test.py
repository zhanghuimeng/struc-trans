import numpy as np
import thumt.data.vocab as vocab
import thumt.utils.helper as helper


def test_gen_typed_matrix_cpu(seq_q, seq_k, vocab_q, vocab_k):
    tensor = helper.gen_typed_matrix_cpu(seq_q, seq_k,
                                         vocab_q, vocab_k)
    tensor = tensor.cpu().numpy()
    return tensor


def test_update_dec_self_attn_batch_cpu(tgt_seq, tgt_vocab):
    batch_size, length = tgt_seq.shape
    mat = np.zeros([3, batch_size, 512, 512], np.int32)
    stack = np.full([batch_size, 512], -1, np.int32)
    stack_pointer = np.full([batch_size], 0, np.int32)
    nearest_q = np.full([batch_size, 512], -1, np.int32)
    stack_history_k = np.full([batch_size, 512, 512], -1, np.int32)
    for i in range(length):
        helper.update_tgt_stack_batch_cpu(
            step=i,
            seq=tgt_seq[:, i],
            stack=stack,
            stack_pointer=stack_pointer,
            nearest_q=nearest_q,
            stack_history_k=stack_history_k,
            vocab=tgt_vocab,
        )
        helper.update_dec_self_attn_batch_cpu(
            step=i,
            mat=mat,
            nearest_q=nearest_q,
            stack_history_k=stack_history_k,
        )
    return mat


def test_update_enc_dec_attn_batch_cpu(src_seq, src_vocab,
                                       tgt_seq, tgt_vocab):
    batch_size, tgt_length = tgt_seq.shape
    mat = np.zeros([3, batch_size, 512, 512], np.int32)
    stack = np.full([batch_size, 512], -1, np.int32)
    stack_pointer = np.full([batch_size], 0, np.int32)
    nearest_q = np.full([batch_size, 512], -1, np.int32)
    stack_history_k = np.full([batch_size, 512, 512], -1, np.int32)

    helper.calc_stack_history_batch_cpu(src_seq, stack_history_k, src_vocab)

    for i in range(tgt_length):
        helper.update_tgt_stack_batch_cpu(
            step=i,
            seq=tgt_seq[:, i],
            stack=stack,
            stack_pointer=stack_pointer,
            nearest_q=nearest_q,
            vocab=tgt_vocab,
        )
        helper.update_enc_dec_attn_batch_cpu(
            step=i,
            length_k=src_seq.shape[1],
            mat=mat,
            nearest_q=nearest_q,
            stack_history_k=stack_history_k,
        )
    return mat


def print_attn_mat(tensor):
    print(np.squeeze(tensor[0]) * 1 + np.squeeze(tensor[1]) * 2 + np.squeeze(tensor[2]) * 3)


src_vocab, tgt_vocab = vocab.load_tagged_vocabulary(
    ["data/example.src.vocab", "data/example.tgt.vocab"])

src_sent_list = [["x", "x", "<a2>", "x", "x", "x", "x", "<i>", "x", "x", "x", "x", "</i>", "</a2>", "x", "<a1>", "x", "x", "</a1>", "x"],
                 ["<i>", "<a1>", "<a2>", "</a2>", "</a1>", "</i>"]]
tgt_sent_list = [["x", "x", "x", "<a1>", "x", "</a1>", "<a2>", "x", "<i>", "x", "x", "</i>", "x", "x", "</a2>", "x"],
                 ["<i>", "</i>", "<a1>", "</a1>", "<a2>", "</a2>"]]

src_sent_list = [[src_vocab["word2idx"][token] for token in line] for line in src_sent_list]
tgt_sent_list = [[tgt_vocab["word2idx"][token] for token in line] for line in tgt_sent_list]

pad_id = src_vocab["word2idx"]["<pad>"]
pad = len(max(src_sent_list, key=len))
src_sent = np.array([i + [0] * (pad - len(i)) for i in src_sent_list])

pad_id = tgt_vocab["word2idx"]["<pad>"]
pad = len(max(tgt_sent_list, key=len))
tgt_sent = np.array([i + [0] * (pad - len(i)) for i in tgt_sent_list])

dec_self_attn_0 = test_gen_typed_matrix_cpu(tgt_sent, tgt_sent, tgt_vocab, tgt_vocab)
enc_dec_attn_0 = test_gen_typed_matrix_cpu(tgt_sent, src_sent, tgt_vocab, src_vocab)

src_length = src_sent.shape[1]
tgt_length = tgt_sent.shape[1]
dec_self_attn_1 = test_update_dec_self_attn_batch_cpu(tgt_sent, tgt_vocab)
dec_self_attn_1 = dec_self_attn_1[:, :, :tgt_length, :tgt_length]
enc_dec_attn_1 = test_update_enc_dec_attn_batch_cpu(
    src_sent, src_vocab, tgt_sent, tgt_vocab)
enc_dec_attn_1 = enc_dec_attn_1[:, :, :tgt_length, :src_length]

assert (dec_self_attn_0 == dec_self_attn_1).all()
assert (enc_dec_attn_0 == enc_dec_attn_1).all()
