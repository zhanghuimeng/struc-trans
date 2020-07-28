#! /usr/bin/env python

import argparse
import sys
import random

DEBUG = False
LOG = False


def show_sent_pair(srcWordList,
                   trgWordList,
                   alignment):
    '''Show a sentence pair.'''
    sys.stdout.write('[srcWordList] ')
    for i in range(len(srcWordList)):
        sys.stdout.write(srcWordList[i] + '/' + str(i))
        if i != len(srcWordList) - 1:
            sys.stdout.write(' ')
    sys.stdout.write('\n[trgWordList] ')
    for i in range(len(trgWordList)):
        sys.stdout.write(trgWordList[i] + '/' + str(i))
        if i != len(trgWordList) - 1:
            sys.stdout.write(' ')
    sys.stdout.write('\n[alignment] ')
    for i in range(len(alignment)):
        sys.stdout.write(str(alignment[i][0]) + \
                         '-' + \
                         str(alignment[i][1]))
        if i != len(alignment) - 1:
            sys.stdout.write(' ')
        else:
            sys.stdout.write('\n')


def extract_phrase_pair(srcWordList,
                        trgWordList,
                        alignment):
    '''Extract phrase pairs.'''
    lenLimit = 5
    phrasePairList = []
    srcAlign = [set() for _ in range(len(srcWordList))]
    trgAlign = [set() for _ in range(len(trgWordList))]
    for a in alignment:
        srcAlign[a[0]].add(a[1])
        trgAlign[a[1]].add(a[0])
    for sb in range(len(srcWordList)):
        for se in range(sb, len(srcWordList)):
            if se - sb + 1 > lenLimit:
                break
            tb, te = -1, -1
            for s in range(sb, se+1):
                for t in srcAlign[s]:
                    if tb == -1 or t < tb:
                        tb = t
                    if te == -1 or t > te:
                        te = t
            if tb == -1 or te == -1:
                continue
            if te - tb + 1 > lenLimit:
                continue
            consistent = True
            for t in range(tb, te+1):
                for s in trgAlign[t]:
                    if s < sb or s > se:
                        consistent = False
                        break
                if not consistent:
                    break
            if not consistent:
                continue
            # Add empty alignment
            while tb > 0:
                if len(trgAlign[tb-1]) == 0:
                    tb -= 1
                else:
                    break
            while te < len(trgWordList) - 1:
                if len(trgAlign[te+1]) == 0:
                    te += 1
                else:
                    break
            phrasePairList.append((sb, se, tb, te))
    return phrasePairList


def show_phrase_pair(srcWordList, trgWordList, alignment, phrasePairList):
    '''Show phrase pairs.'''
    print('\nThe phrase pair list is:')
    for pp in phrasePairList:
        sys.stdout.write(str(pp) + ': ')
        for i in range(pp[0], pp[1] + 1):
            sys.stdout.write(srcWordList[i] + \
                             '/' + \
                             str(i) + \
                             ' ')
        sys.stdout.write('<---> ')
        for i in range(pp[2], pp[3] + 1):
            sys.stdout.write(trgWordList[i] + \
                             '/' + \
                             str(i) + \
                             ' ')
        sys.stdout.write('\n')


def select_phrase_pair(phrasePairList):
    """
	Select phrase pair.
	:param phrasePairList: 
	:return: 
	"""
    selected = []
    for pp1 in phrasePairList:
        if random.random() > 0.3:
            continue
        # TODO: define your rules here
        # Avoid single letters
        if pp1[0] == pp1[1] or \
                pp1[2] == pp1[3]:
            continue

        overlap = False
        for pp2 in selected:
            if pp2[0] <= pp1[0] <= pp2[1] or \
                    pp2[0] <= pp1[1] <= pp2[1] or \
                    pp2[2] <= pp1[2] <= pp2[3] or \
                    pp2[2] <= pp1[3] <= pp2[3]:
                overlap = True
                break
        if not overlap:
            selected.append(pp1)
    return selected


def gen_result(srcWordList,
               trgWordList,
               alignment,
               selected,
               resultSrcFile,
               resultTrgFile):
    '''Generate result.'''
    taggedSrcWordList = []
    taggedTrgWordList = []
    for i in range(len(srcWordList)):
        head, tail = -1, -1
        for j in range(len(selected)):
            if i == selected[j][0]:
                head = j + 1
                break
            if i == selected[j][1]:
                tail = j + 1
                break
        if head != -1:
            taggedSrcWordList.append('<a' + str(head) + '>')
        taggedSrcWordList.append(srcWordList[i])
        if tail != -1:
            taggedSrcWordList.append('</a' + str(tail) + '>')
    for i in range(len(trgWordList)):
        head, tail = -1, -1
        for j in range(len(selected)):
            if i == selected[j][2]:
                head = j + 1
                break
            if i == selected[j][3]:
                tail = j + 1
                break
        if head != -1:
            taggedTrgWordList.append('<a' + str(head) + '>')
        taggedTrgWordList.append(trgWordList[i])
        if tail != -1:
            taggedTrgWordList.append('</a' + str(tail) + '>')
    if LOG:
        print('\n[taggedSrcWordList]', ' '.join(taggedSrcWordList))
        print('[taggedTrgWordList]', ' '.join(taggedTrgWordList))

    resultSrcFile.write(' '.join(taggedSrcWordList) + '\n')
    resultTrgFile.write(' '.join(taggedTrgWordList) + '\n')

    return taggedSrcWordList


def add_tag(srcFileName,
            trgFileName,
            agtFileName,
            resultSrcFileName,
            resultTrgFileName):
    '''Add tags.'''
    srcFile = open(srcFileName, 'r', encoding='UTF-8')
    trgFile = open(trgFileName, 'r', encoding='UTF-8')
    agtFile = open(agtFileName, 'r', encoding='UTF-8')
    resultSrcFile = open(resultSrcFileName, 'w', encoding='UTF-8')
    resultTrgFile = open(resultTrgFileName, 'w', encoding='UTF-8')

    cnt = 0
    backLongCnt = 0
    nowLongCnt = 0
    while True:
        cnt += 1
        line1 = srcFile.readline()
        line2 = trgFile.readline()
        line3 = agtFile.readline()
        if line1 == '' or \
                line2 == '' or \
                line3 == '':
            break
        # build source word list, target word list, and word alignment
        srcWordList = line1.split()
        trgWordList = line2.split()
        alignment = []
        for x in line3.split():
            sp = int(x.split('-')[0])
            tp = int(x.split('-')[1])
            alignment.append((sp, tp))
        if DEBUG:
            show_sent_pair(srcWordList, trgWordList, alignment)
        # extract phrase pairs
        phrasePairList = extract_phrase_pair(srcWordList,
                                             trgWordList,
                                             alignment)
        if DEBUG:
            show_phrase_pair(srcWordList,
                             trgWordList,
                             alignment,
                             phrasePairList)
        # randomly select some phrase pairs
        selected = select_phrase_pair(phrasePairList)
        if DEBUG:
            sys.stdout.write('\nSelected: ' + \
                             ' '.join([str(pp) for pp in selected]) +
                             '\n')
        # generate the result
        taggedSrcWordList = gen_result(
            srcWordList=srcWordList,
            trgWordList=trgWordList,
            alignment=alignment,
            selected=selected,
            resultSrcFile=resultSrcFile,
            resultTrgFile=resultTrgFile
        )

        if len(srcWordList) > 256:
            backLongCnt += 1
        if len(taggedSrcWordList) > 256:
            nowLongCnt += 1
        if cnt % 10000 == 0:
            print("%d: %f/%f" % (cnt, backLongCnt/cnt, nowLongCnt/cnt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--src_file", type=str, help="src input file",
        default="data/UN-zh-en/valid.zh.tok"
    )
    parser.add_argument(
        "--trg_file", type=str, help="trg input file",
        default="data/UN-zh-en/valid.en.tok"
    )
    parser.add_argument(
        "--align_file", type=str, help="alignment file",
        default="data/UN-zh-en/valid.final.align"
    )
    parser.add_argument(
        "--output_src_file", type=str, help="src output file",
        default="data/UN-zh-en/valid.tagged.zh"
    )
    parser.add_argument(
        "--output_trg_file", type=str, help="trg output file",
        default="data/UN-zh-en/valid.tagged.en")
    args = parser.parse_args()

    add_tag(
        srcFileName=args.src_file,
        trgFileName=args.trg_file,
        agtFileName=args.align_file,
        resultSrcFileName=args.output_src_file,
        resultTrgFileName=args.output_trg_file
    )
