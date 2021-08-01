# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare
# Package to extract per base GC Content
#
import sys
from typing import TextIO

import numpy as np
from pycparser.ply.cpp import xrange


def extract_perbase_GCContentRowsFromFastQC(filepointer: TextIO, line: str, resultsdata: dict, per_base_gc_content: list[str]) -> tuple[TextIO, dict, dict]:
    try:
        # Extended to extract additional data ######
        if filepointer & line & resultsdata & line.startswith('>>Per base GC content'):
            resultsdata['perperbasegccontent'] = {}
            resultsdata['perperbasegccontent']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['perperbasegccontent']['perbasegccontentrows'] = []
            perbasegcrows: list[str] = resultsdata['perperbasegccontent']['perbasegccontentrows']

            # Get header row
            resultsdata['perperbasegccontent']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows # Split the ranges as individual values
            # Create dictionary per base
            nextrow = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                nextrow = filepointer.readline()
                perbasegcrows.append(nextrow.rstrip().split('\t'))
                vals: list[str] = nextrow.strip().split('\t')
                if '-' in vals[0]:
                    minvals: int
                    minvals, maxvals = vals[0].strip().split('-')
                    for x in xrange(int(minvals), int(maxvals)):
                        per_base_gc_content['rows'][x] = float(vals[1])
                else:
                    if '>>' not in vals[0]:
                        per_base_gc_content['rows'][int(vals[0])] = float(vals[1])
                continue
        if per_base_gc_content:
            return filepointer, resultsdata, per_base_gc_content
        else:
            raise Exception("Error encountered while parsing GC Content rows")
    except Exception as exception:
        print("Exception while parsing GC Content rows %s" % exception)
    finally:
        print("Finished parsing GC Content rows")


def perbasegccontent(resultsdata: dict) -> tuple[dict, dict]:
    """

    :rtype: object
    """
    # print "###Per base GC Content###"
    # header and 3 intervals
    perbasegccontent['header'] = resultsdata['perperbasegccontent']['header']
    counter = 0
    for listiterator in np.array_split(perbasegccontent['rows'].keys(), 3):
        counter += 1
        subdict: dict = {rowentry: perbasegccontent['rows'][rowentry] for rowentry in listiterator if rowentry in perbasegccontent['rows']}
        for key in subdict.keys():
            perbasegccontent['intervals' + str(counter)][key] = subdict[key]
        perbasegccontent['interval' + str(counter) + 'avg'] = np.average(subdict.values())
        # entire results, not needed
        # results = {'fastqc': resultsdata}
    if perbasegccontent:
        try:
            del perbasegccontent['rows']
            resultsperbasegccontent = {'fastqcperbasegccontent': perbasegccontent}
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

    return perbasegccontent, resultsperbasegccontent
