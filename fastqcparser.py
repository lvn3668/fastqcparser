#!/usr/local/bin python
# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare

import sys
import json
from argparse import ArgumentParser
from typing import TextIO, Dict, Any

import numpy as np

import basicstatistics as basestats
import utilities as util
import per_base_seq_quality as pbq
import per_base_GC_Content as pbgccontent
import pertilesequencequality as ptseqqual
import per_sequence_quality_scores as perseqqualscores
import per_base_sequence_content.extractperbaseSequenceContentFromFastQC as perbaseseqcontent
import kmer_content.extractKmerContentlinesFromFastQC as kmerc
import adaptercontent as adaptcont
import per_base_NContent as pbNContent
import per_base_seq_quality as perbaseseqqual


# from pprint import pprint
# import errno

def parse_fastqc_data(file: TextIO) -> object:
    try:
        with open(file) as filepointer:
            while True:
                line = filepointer.readline()
                if not line: break
                if line.startswith('##FastQC'):
                    resultsdata["fastqcversion"] = line.split()[1]
                    continue

                basicstatistics: dict
                results_perbase_sequencecontentA: dict
                perbasegccontent: dict
                tilingrows: dict
                results_perbase_sequencecontentC: dict
                Adaptercontentrows: dict
                perbasesequencequality: list[str]
                basicstatistics, perbasesequencequality, perbasegccontent, tilingrows, \
                results_perbase_sequencecontentA, \
                results_perbase_sequencecontentT, results_perbase_sequencecontentG, \
                results_perbase_sequencecontentC, Ncontentrows, Adaptercontentrows, KMercontentrows, \
                perbasesequencecontentA, perbasesequencecontentT, perbasesequencecontentG, \
                perbasesequencecontentC, resultsdata = util.initialize()

                filepointer: filepointer
                ####################################################################################
                filepointer, resultsdata, basicstatistics = basestats.extractBasicStatisticsLinesFromFastQC(line,
                                                                                                            resultsdata,
                                                                                                            basicstatistics)
                assert (len(basicstatistics) != 0), "Basic Statistics lines are empty"
                ####################################################################################
                filepointer, resultsdata, perbasesequencequality = \
                    pbq.extractperbasesequencequalityFromFastQC(filepointer, line, resultsdata, perbasesequencequality)

                assert (len(perbasesequencequality) != 0), "Per base sequence quality is empty"
                ####################################################################################
                perbasegccontent: list[str]
                filepointer, resultsdata, perbasegccontent = \
                    pbgccontent.extract_perbase_GCContentRowsFromFastQC(filepointer, line, resultsdata,
                                                                        perbasegccontent)

                assert (len(perbasegccontent) != 0), "Per base GC Content is empty"
                ####################################################################################
                filepointer, resultsdata, tilingrows = ptseqqual.extract_pertile_sequence_quality_records_from_FastQC(
                    filepointer, line, resultsdata,
                    tilingrows)
                assert (len(tilingrows) != 0), "Tiling row entries is empty"
                ####################################################################################
                filepointer, resultsdata, perbasesequencequality = perseqqualscores.perseqqualityscores(filepointer,
                                                                                                        line,
                                                                                                        resultsdata,
                                                                                                        perbasesequencequality)
                assert (len(perbasesequencequality) != 0), "Per base sequence quality is empty"
                ####################################################################################
                filepointer, resultsdata, perbasesequencecontentA, \
                perbasesequencecontentT, perbasesequencecontentG, \
                perbasesequencecontentC = perbaseseqcontent.extract_perbase_sequence_content(filepointer,
                                                                                             line, resultsdata,
                                                                                             perbasesequencecontentA,
                                                                                             perbasesequencecontentT,
                                                                                             perbasesequencecontentG,
                                                                                             perbasesequencecontentC)
                assert (len(perbasesequencecontentA) != 0), "Per-base sequence content (A) is empty"
                assert (len(perbasesequencecontentT) != 0), "Per-base sequence content (T) is empty"
                assert (len(perbasesequencecontentG) != 0), "Per-base sequence content (G) is empty"
                assert (len(perbasesequencecontentC) != 0), "Per-base sequence content (C) is empty"
                ####################################################################################
                Ncontentrows: list[str]
                assert isinstance(Ncontentrows, list)
                filepointer, resultsdata, Ncontentrows = pbNContent.getperbaseNContent(filepointer,
                                                                                       line, resultsdata,
                                                                                       Ncontentrows)
                assert (len(Ncontentrows) != 0), "Length of N Content rows is empty"
                ####################################################################################
                AdapterContentrows: list[str]
                assert isinstance(AdapterContentrows, list)
                filepointer, resultsdata, AdapterContentrows = adaptcont.extractAdapterContentrows(filepointer, line,
                                                                                                   resultsdata,
                                                                                                   AdapterContentrows)
                assert (len(AdapterContentrows) != 0), "Adapter Content rows is empty"
                ####################################################################################
                # Skip line with "Measure  Value" labels
                nextrow = filepointer.readline()
                if nextrow.startswith('#Measure'):
                    nextrow = filepointer.readline()

                    while not nextrow.startswith('>>END_MODULE'):
                        parts = nextrow.rstrip().split('\t')
                        key = parts[0]
                        value = parts[1]
                        basicstatistics[key] = value
                    nextrow = filepointer.readline()
                    continue
                ####################################################################################
                KMercontentrows: list[str]
                assert isinstance(KMercontentrows, list)
                filepointer, resultsdata, KMercontentrows = kmerc.extractKMerContentLines(filepointer,
                                                                                          line,
                                                                                          resultsdata,
                                                                                          KMercontentrows)

                assert len(KMercontentrows) != 0, "Length of KMer content rows is empty"
                ####################################################################################
                # calculateaveragesequencequalityoverintervals
                assert isinstance(perbasesequencecontentT, dict)
                assert isinstance(perbasesequencecontentA, dict)
                assert isinstance(perbasesequencecontentG, dict)
                assert isinstance(perbasesequencecontentC, dict)
                assert isinstance(results_perbase_sequencecontentA, dict)
                assert isinstance(results_perbase_sequencecontentT, dict)
                assert isinstance(results_perbase_sequencecontentG, dict)
                assert isinstance(results_perbase_sequencecontentC, dict)
                results_perbase_sequencecontentA, results_perbase_sequencecontentT, \
                results_perbase_sequencecontentG, results_perbase_sequencecontentC, \
                perbasesequencecontentA, perbasesequencecontentT,
                perbasesequencecontentG, perbasesequencecontentC = \
                    perbaseseqqual.calculateaveragesequencequalityoverintervals(
                        perbasesequencequality, resultsdata,
                        perbasesequencecontentA,
                        perbasesequencecontentT,
                        perbasesequencecontentG,
                        perbasesequencecontentC)
                ####################################################################################
                results_perbase_gc_content = pbgccontent.perbasegccontent(resultsdata)
                if perbasesequencequality:
                    try:
                        del perbasesequencequality['rows']
                        results_perbase_sequencequality: dict[str, dict] = {
                            'fastqcperbasesequencequality': perbasesequencequality}
                    except Exception:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise Exception(sys.exc_info()[0])

                imagefile: np.uint8 = None  # Can be deleted. To be confirmed
    except (FileNotFoundError, IOError):
        print(" File Not Found")

    return (resultsdata, results_perbase_gc_content, results_perbase_sequencecontentC, results_perbase_sequencecontentT,
            results_perbase_sequencecontentG, results_perbase_sequencecontentA, results_perbase_sequencequality,
            imagefile)


########################################################################
def parse_fastqc_data_wrapper(fastqcfilename: TextIO):
    """

    :type fastqcfilename: object
    """
    fastqcparserresults: dict[str, dict] = {}
    (results_data, results_perbase_gccontent, results_perbase_sequencecontentC, results_perbase_sequencecontentT,
     results_perbase_sequencecontentG, results_perbase_sequencecontentA, results_perbase_sequencequality,
     imagefiles) = parse_fastqc_data(fastqcfilename)
    # fastqcparserresults['allresults'] =  results_data
    # We are not storing all results_data
    try:
        if results_perbase_gccontent:
            fastqcparserresults['results_perbase_gccontent'] = results_perbase_gccontent
        if results_perbase_sequencecontentC:
            fastqcparserresults['results_perbase_sequencecontentC'] = results_perbase_sequencecontentC
        if results_perbase_sequencecontentT:
            fastqcparserresults['results_perbase_sequencecontentT'] = results_perbase_sequencecontentT
        if results_perbase_sequencecontentG:
            fastqcparserresults['results_perbase_sequencecontentG'] = results_perbase_sequencecontentG
        if results_perbase_sequencecontentA:
            fastqcparserresults['results_perbase_sequencecontentA'] = results_perbase_sequencecontentA
        if results_perbase_sequencequality:
            fastqcparserresults['results_perbase_sequencequality'] = results_perbase_sequencequality
    except Exception as exceptn:
        print("Unexpected error %s" % exceptn)

    # No image files either
    # fastqcparserresults['imagesfiles'] = None

    if not util.is_json(json.dumps(fastqcparserresults)):
        raise Exception(sys.exc_info()[0])
    return json.dumps(fastqcparserresults)


########################################################################
if __name__ == '__main__':
    try:

        table_lookup = {
            'perbasesqqualityrows': 'fastqc_per_base_sequencing_quality',
            'pertileseqqualityrows': 'fastqc_per_tile_seq_quality',
            'perseqqualityrows': 'fastqc_per_seq_quality',
            'perbaseseqcontentrows': 'fastqc_per_base_seq_content',
            'perbaseNcontentrows': 'fastqc_per_base_NContent',
            'AdapterContentrows': 'fastqc_adapterContent',
            'basicstatisticsdata': 'fastqc_basicstatistics',
            'KmerContentrows': 'fastqc_kmercontent'
        }

        parser = ArgumentParser()
        parser.add_argument('fastqcfilename')
        parser.add_argument('sampleid')
        parser.add_argument('runid')
        # parser.add_argument('sqlfilename')
        # parser.add_argument('tablename')
        args = parser.parse_args()
        (results, resultsperbasegccontent, resultsperbasesequencecontentC, resultsperbasesequencecontentT,
         resultsperbasesequencecontentG, resultsperbasesequencecontentA, resultsperbasesequencequality,
         imagefiles) = parse_fastqc_data(args.fastqcfilename)
        # Removed all subsequent writes to file, etc.
    except Exception as exception:
        print("Error encountered parsing FastQC results %s " % exception)
    finally:
        print("FastQC parser completed successfully")
