#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division, print_function)
from six import reraise as raise_
import sys
import time
import pandas as pd
import logging


logger = logging.getLogger("STAR-SEQR")


def make_bedpe_line(df, bedpe_fh):
    chrom1, pos1, str1, chrom2, pos2, str2, repleft, repright = re.split(':', df['name'])
    pos1 = int(pos1)
    pos2 = int(pos2)
    end1 = pos1 + 1
    end2 = pos2 + 1
    score = df['span_first'] + df['jxn_left']
    quant = "."
    fusion_class = df['Fusion_Class']
    bedpe_stuff = [chrom1, pos1, end1, chrom2, pos2, end2, name, score, str1, str2, quant]
    bedpe_line = '\t'.join(map(str,(bedpe_stuff)))
    print(bedpe_line, bedpe_fh)
    return


def write_bedpe(df, out_bedpe, args):
    '''the bedpe should be 0 based, incoming values are 0 based.'''
    bedpe_path = args.prefix + '_STAR-SEQR_breakpoints.bedpe'
    bedpe_fh = open(bedpe_path, 'w')
    write_header(args, bedpe_fh, "bedpe")
    if len(df.index) >= 1:
        df.apply(lambda x: make_bedpe_line(df, bedpe_fh), axis=1)
    bedpe_fh.close()
    logger.info("Wrote bedpe Successfully!")
    return
