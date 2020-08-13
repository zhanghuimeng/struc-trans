import argparse
import os

def gizapp(args):
    os.system("mkdir gizapp")
    os.chdir(os.getcwd() + "/gizapp")
    print(os.getcwd())
    # 文本单词编号
    os.system("/data/disk5/private/zhm/202007_struc/dep/plain2snt.out ../%s ../%s" % (args.src_file, args.trg_file))
    # 生成共现文件
    os.system("/data/disk5/private/zhm/202007_struc/dep/snt2cooc.out %s.vcb %s.vcb %s_%s.snt > zh_en.cooc" % (args.src_file, args.trg_file, args.src_file, args.trg_file))
    os.system("/data/disk5/private/zhm/202007_struc/dep/snt2cooc.out %s.vcb %s.vcb %s_%s.snt > en_zh.cooc" % (args.trg_file, args.src_file, args.trg_file, args.src_file))
    # 生成词类
    os.system("/data/disk5/private/zhm/202007_struc/dep/mkcls -p%s -V%s.vcb.classes opt" % (args.src_file, args.src_file))
    os.system("/data/disk5/private/zhm/202007_struc/dep/mkcls -p%s -V%s.vcb.classes opt" % (args.trg_file, args.trg_file))
    # GIZA++进行词对齐，事先创建e2z和z2e目录
    os.system("mkdir z2e")
    os.system("mkdir e2z")
    os.system("/data/disk5/private/zhm/202007_struc/dep/GIZA++ -S %s.vcb -T %s.vcb -C %s_%s.snt -CoocurrenceFile zh_en.cooc -o z2e -OutputPath z2e" % (args.src_file, args.trg_file, args.src_file, args.trg_file))
    os.system("/data/disk5/private/zhm/202007_struc/dep/GIZA++ -S %s.vcb -T %s.vcb -C %s_%s.snt -CoocurrenceFile en_zh.cooc -o e2z -OutputPath e2z" % (args.trg_file, args.src_file, args.trg_file, args.src_file))
    # 提取对齐信息
    print(os.getcwd())
    os.system("python /data/disk5/private/zhm/202007_struc/dep/extract.py -i gizapp/z2e/z2e.A3.final -o gizapp/z2e.A3.final.extract -r")
    os.system("python /data/disk5/private/zhm/202007_struc/dep/extract.py -i gizapp/e2z/e2z.A3.final -o gizapp/e2z.A3.final.extract")
    # 对齐
    os.system("/data/disk5/private/zhm/202007_struc/dep/fast_align/build/atools -i z2e.A3.final.extract -j e2z.A3.final.extract -c grow-diag-final-and > giza_alignment.out")
    os.chdir("..")

def fastalign(args):
    os.system("mkdir fastalign")
    os.chdir(os.getcwd() + "/fastalign")
    # 整理格式
    os.system("python /data/disk5/private/zhm/202007_struc/dep/fastalign_interleave.py --left_file ../%s --right_file ../%s --output train.zh-en" % (args.src_file, args.trg_file))
    # Fast Align
    os.system("/data/disk5/private/zhm/202007_struc/dep/fast_align/build/fast_align -i train.zh-en -d -o -v > forward.align")
    os.system("/data/disk5/private/zhm/202007_struc/dep/fast_align/build/fast_align -i train.zh-en -d -o -v -r > reverse.align")
    os.system("/data/disk5/private/zhm/202007_struc/dep/fast_align/build/atools -i forward.align -j reverse.align -c grow-diag-final-and > fastalign_alignment.out")
    os.chdir("..")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src_file", type=str, help="src input file",
    default="nist02.zh"
)
parser.add_argument(
    "--trg_file", type=str, help="trg input file",
    default="nist02.en"
)
args = parser.parse_args()

# gizapp(args)
fastalign(args)

# os.system("python /data/disk5/private/zhm/202007_struc/dep/ensemble_alignments.py --alignments gizapp/giza_alignment.out fastalign/fastalign_alignment.out --output ensemble_alignment.out")

os.system("cp fastalign/fastalign_alignment.out ensemble_alignment.out")
