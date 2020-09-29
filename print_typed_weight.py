import argparse
import torch
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument(
    "--checkpoint", type=str, help="src input file",
    default="train/model-100.pt"
)
parser.add_argument(
    "--save_path", type=str, help="src input file",
    default="data/figure/"
)
args = parser.parse_args()

templates = ["encoder.layers.%d.self_attention.attention.typed_weight",
             "decoder.layers.%d.self_attention.attention.typed_weight",
             "decoder.layers.%d.encdec_attention.attention.typed_weight"]
names = ["std", "in", "out"]
checkpoint = torch.load(args.checkpoint)
for i in range(3):
    for j in range(6):
        typed_weight = checkpoint["model"][templates[i] % j].cpu().numpy()
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        for k in range(3):
            x = np.reshape(typed_weight[k], [-1])
            ax.hist(x, 50, density=True, label=names[k])
            ax.legend()
            fig.canvas.draw()
        plt.savefig(args.save_path + templates[i] % j + ".png")
