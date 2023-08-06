#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
import sys
import logging
import subprocess as sp
import re
import starseqr_utils as su

logger = logging.getLogger('STAR-SEQR')

# http://deweylab.biostat.wisc.edu/rsem/rsem-prepare-reference.html
# http://deweylab.biostat.wisc.edu/rsem/rsem-calculate-expression.html

def rsem_prep_calc():
    cmd = "rsem-prepare-reference --transcript-to-gene-map "+out_path+"transcript_list.txt  --no-polyA "+out_path +"transcript_seq.fa "+name_output;
    # * transcript_list is gene/tisoform


    cmd = "rsem-calculate-expression -p "+thread_num+" --paired-end --keep-intermediate-files "+file1+" "+file2+" "+name_output+" "+exp_output;
    # * input can be fastq(default), --sam, --bam
    # * --strand-specific option exists
    # -p threads
    # --no-bam0ouput

# subset bam to primary.sam as follows: samtools view -F 256  supporting.bam | sort -k1


def run_rsem(jxn, as_type):
    # clean jxn name to write to support folder made previous
    clean_jxn = su.common.safe_jxn(jxn)
    jxn_dir = 'support' + '/' + clean_jxn + '/'

    fusionfq = jxn_dir + 'transcripts_all_fusions.fa'

    pairfq = jxn_dir + 'paired.fastq'
    junctionfq = jxn_dir + 'junctions.fastq'
