# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare
import sys
from typing import Any, Union, Optional, TextIO

import numpy as np
from pycparser.ply.cpp import xrange


def extractperbasesequencequalityFromFastQC(filepointer: TextIO, line: str, resultsdata: dict,
                                            perbasesequencequality: list[str]) -> tuple[TextIO, dict, list[str]]:
    """

    :rtype: object
    :param filepointer: 
    :param line: 
    :param resultsdata: 
    :param perbasesequencequality: 
    :return: 
    """
    try:
        if line.startswith('>>Per base sequence quality'):
            resultsdata['perperbasesequencequality'] = {}
            resultsdata['perperbasesequencequality']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['perperbasesequencequality']['perbasesqqualityrows'] = []
            perbaserows: list[str] = resultsdata['perperbasesequencequality']['perbasesqqualityrows']

            # Get header row
            resultsdata['perperbasesequencequality']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows # Extract only the mean
            # Create dictionary per base
            nextrow = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                nextrow = filepointer.readline()
                perbaserows.append(nextrow.rstrip().split('\t'))
                vals: Any = nextrow.strip().split('\t')
                if '-' in vals[0]:
                    minval: int
                    maxval: int
                    minval, maxval = vals[0].strip().split('-')
                    for x in xrange(int(minval), int(maxval)):
                        perbasesequencequality['rows'][x] = float(vals[1])
                else:
                    if '>>' not in vals[0]:
                        perbasesequencequality['rows'][int(vals[0])] = float(vals[1])
                continue
        if perbasesequencequality:
            return filepointer, resultsdata, perbasesequencequality
        else:
            raise Exception("Error in extracting per base sequence quality")
    except Exception as exception:
        print("Extracting per base sequence quality records failed %s" % exception)
    finally:
        print("Extracting per base sequence quality records from FastQC records completed")


def calculate_avg_seqqual_over_interval(indexnumber: int, perbasesequencequality: list[str],
                                        resultsdata: dict, numintervals: int, perbasesequencecontent: dict) -> dict:
    """

    :type numintervals: int
    :param perbasesequencecontent: 
    :param numintervals: 
    :param resultsdata: 
    :param perbasesequencequality: 
    :type indexnumber: object
    """
    try:
        # Gets the header
        perbasesequencequality['header'] = [resultsdata['perperbasesequencequality']['header'][0],
                                            resultsdata['perperbasesequencequality']['header'][1]]
        # Creates the 3 intervals
        counter = 0
        for list in np.array_split(perbasesequencequality['rows'].keys(), numintervals):
            counter += 1
            subdict: dict = {y: perbasesequencequality['rows'][y] for y in list if y in perbasesequencequality['rows']}
            for key in subdict.keys():
                perbasesequencequality['intervals' + str(counter)][key] = subdict[key]
            perbasesequencequality['interval' + str(counter) + 'avg'] = np.average(subdict.values())

        perbasesequencecontent['header'] = [resultsdata['per_base_sequence_content']['header'][0],
                                            resultsdata['per_base_sequence_content']['header'][indexnumber]]
        counter = 0
        for list in np.array_split(perbasesequencecontent['rows'].keys(), numintervals):
            counter += 1
            subdict = {y: perbasesequencecontent['rows'][y] for y in list if y in perbasesequencecontent['rows']}
            for key in subdict.keys():
                perbasesequencecontent['intervals' + str(counter)][key] = subdict[key]
            perbasesequencecontent['interval' + str(counter) + 'avg'] = np.average(subdict.values())
        if perbasesequencecontent:
            return perbasesequencecontent
        else:
            raise Exception("Error encountered in extracting per base sequence content %s")
    except Exception as exception:
        print("Exception encountered %s " % exception)
    finally:
        print("Calculation of average sequence quality over each interval completed")


def calculateaveragesequencequalityoverintervals(perbasesequencequality: list[str], resultsdata: dict,
                                                 perbasesequencecontentA: dict,
                                                 perbasesequencecontentT: dict,
                                                 perbasesequencecontentG: dict,
                                                 perbasesequencecontentC: dict) -> tuple[
    dict, dict, dict, dict, dict, dict, dict, dict]:
    """

    :param perbasesequencequality: 
    :param resultsdata: 
    :param perbasesequencecontentA: 
    :param perbasesequencecontentT: 
    :param perbasesequencecontentG: 
    :param perbasesequencecontentC: 
    :return: 
    """
    perbasesequencecontentA = calculate_avg_seqqual_over_interval(2, perbasesequencequality, resultsdata, 3,
                                                                  perbasesequencecontentA)
    perbasesequencecontentT = calculate_avg_seqqual_over_interval(3, perbasesequencequality, resultsdata, 3,
                                                                  perbasesequencecontentT)
    perbasesequencecontentG = calculate_avg_seqqual_over_interval(1, perbasesequencequality, resultsdata, 3,
                                                                  perbasesequencecontentG)
    perbasesequencecontentC = calculate_avg_seqqual_over_interval(4, perbasesequencequality, resultsdata, 3,
                                                                  perbasesequencecontentC)

    resultsperbasesequencecontentA: dict = {}
    resultsperbasesequencecontentT: dict = {}
    resultsperbasesequencecontentG: dict = {}
    resultsperbasesequencecontentC: dict = {}
    if perbasesequencecontentC:
        try:
            del perbasesequencecontentC['rows']
            resultsperbasesequencecontentC = {'fastqcpersequenceCcontent': perbasesequencecontentC}
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

    if perbasesequencecontentT:
        try:
            del perbasesequencecontentT['rows']
            resultsperbasesequencecontentT = {'fastqcpersequenceTcontent': perbasesequencecontentT}
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

    if perbasesequencecontentG:
        try:
            del perbasesequencecontentG['rows']
            resultsperbasesequencecontentG = {'fastqcpersequenceGcontent': perbasesequencecontentG}
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

    if perbasesequencecontentA:
        try:
            del perbasesequencecontentA['rows']
            resultsperbasesequencecontentA: dict[
                str, dict[str, Union[Union[list[Any], tuple[Any, Optional[Any]]], Any]]] = {
                'fastqcpersequenceAcontent': perbasesequencecontentA}
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception(sys.exc_info()[0])

    if resultsperbasesequencecontentA & resultsperbasesequencecontentT & resultsperbasesequencecontentG & resultsperbasesequencecontentC:
        return (resultsperbasesequencecontentA, resultsperbasesequencecontentT, resultsperbasesequencecontentC,
                resultsperbasesequencecontentG, perbasesequencecontentA, perbasesequencecontentT,
                perbasesequencecontentG, perbasesequencecontentC)
