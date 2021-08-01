# Author: Lalitha Viswanathan
# Affiliation: Stanford Health Care
from typing import TextIO

from pycparser.ply.cpp import xrange


def extract_perbase_sequence_content(filepointer: TextIO, line: str, resultsdata: dict, perbasesequencecontentA: dict,
                                     perbasesequencecontentT: dict, perbasesequencecontentG: dict,
                                     perbasesequencecontentC: dict):
    if line.startswith('>>Per base sequence content'):
        resultsdata['per_base_sequence_content'] = {}
        resultsdata['per_base_sequence_content']['passfail'] = line.rstrip().split('\t')[1]
        resultsdata['per_base_sequence_content']['perbaseseqcontentrows'] = []
        seqcontentrows: dict = resultsdata['per_base_sequence_content']['perbaseseqcontentrows']

        # Get header row
        resultsdata['per_base_sequence_content']['header'] = filepointer.readline().rstrip().split('\t')

        # Get other rows
        # Per base sequence content to be split as A, T, G, C
        nextrow = filepointer.readline()
        while not nextrow.startswith('>>END_MODULE'):
            nextrow = filepointer.readline()
            seqcontentrows.append(nextrow.rstrip().split('\t'))
            vals: list[str] = nextrow.strip().split('\t')
            if '-' in vals[0]:
                minval: int
                maxval: int
                minval, maxval = vals[0].strip().split('-')
                for x in xrange(int(minval), int(maxval)):
                    perbasesequencecontentA['rows'][x] = float(vals[1])
                    perbasesequencecontentT['rows'][x] = float(vals[2])
                    perbasesequencecontentG['rows'][x] = float(vals[3])
                    perbasesequencecontentC['rows'][x] = float(vals[4])
            else:
                if '>>' not in vals[0]:
                    perbasesequencecontentA['rows'][int(vals[0])] = float(vals[1])
                    perbasesequencecontentT['rows'][int(vals[0])] = float(vals[2])
                    perbasesequencecontentG['rows'][int(vals[0])] = float(vals[3])
                    perbasesequencecontentC['rows'][int(vals[0])] = float(vals[4])
            continue
        return resultsdata, seqcontentrows, perbasesequencecontentA, perbasesequencecontentT, \
               perbasesequencecontentG, perbasesequencecontentC
