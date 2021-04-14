import argparse
import csv
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
from tensorboard.backend.event_processing import tag_types

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input", type=str, help="input summary file",
)
parser.add_argument(
    "--tag", type=str, help="config file",
)
parser.add_argument(
    "--filter", type=int, default=10000, help="output file",
)
parser.add_argument(
    "--name", type=str, nargs=3, help="names of the output",
    default=["WallTime", "step", "4 (1e-4)"],
)
parser.add_argument(
    "--output", type=str, help="output file",
)
args = parser.parse_args()

event_acc = EventAccumulator(args.input, size_guidance={tag_types.SCALARS: 10000000})
event_acc.Reload()
w_times, step_nums, vals = zip(*event_acc.Scalars(args.tag))
N = len(w_times)
print("Steps for all GPUs: %d" % N)

filtered_wtimes = []
filtered_step_nums = []
filtered_vals = []
for i in range(N):
    if i == 0 or step_nums[i] != step_nums[i - 1]:
        filtered_wtimes.append(w_times[i])
        filtered_step_nums.append(step_nums[i])
        filtered_vals.append(vals[i])

N = len(filtered_wtimes)
step = N // args.filter
with open(args.output, mode="w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(args.name)
    for i in range(0, N, step):
        writer.writerow([filtered_wtimes[i], filtered_step_nums[i], filtered_vals[i]])
