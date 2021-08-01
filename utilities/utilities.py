# Author: Lalitha Viswanathan
# Affiliation: Stanford Health Care
#######################################
import json

import numpy as np


#######################################
def duplication_levels(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def kmer_profiles(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def per_base_gc_content(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def per_base_n_content(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def per_base_quality(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def per_base_sequence_content(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def per_sequence_gc_content(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def per_sequence_quality(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise


#######################################
def sequence_length_distribution(imagefile: np.uint8):
    try:
        results: None = None
        return results, imagefile
    except Exception:
        raise

#######################################
def is_json(myjson: json) -> tuple[json, bool]:
    try:
        json_object: json = json.loads(myjson)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None, False
    return json_object, True


#######################################

def initialize() -> tuple[dict, dict, dict, \
                          dict, dict, dict, \
                          dict, dict, dict, \
                          dict, dict, dict, dict, dict, \
                          dict, dict]:
    """

    :rtype: tuple[dict, dict, dict, dict, dict, dict, dict, dict, dict, dict, dict]
    """
    try:
        resultsdata = {}
        basicstatistics: dict = dict()
        tilingrows: dict = dict()
        results_perbase_sequencecontentA: dict = dict()
        results_perbase_sequencecontentT: dict = dict()
        results_perbase_sequencecontentG: dict = dict()
        results_perbase_sequencecontentC: dict = dict()
        # Assuming division into 3 intervals only
        perbasesequencequality = {'header': [], 'rows': {}, 'intervals1': {}, 'intervals2': {}, 'intervals3': {}}
        perbasesequencecontentA = {'header': [], 'rows': {}, 'intervals1': {}, 'intervals2': {}, 'intervals3': {}}
        perbasesequencecontentT = {'header': [], 'rows': {}, 'intervals1': {}, 'intervals2': {}, 'intervals3': {}}
        perbasesequencecontentG = {'header': [], 'rows': {}, 'intervals1': {}, 'intervals2': {}, 'intervals3': {}}
        perbasesequencecontentC = {'header': [], 'rows': {}, 'intervals1': {}, 'intervals2': {}, 'intervals3': {}}
        perbasegccontent = {'header': [], 'rows': {}, 'intervals1': {}, 'intervals2': {}, 'intervals3': {}}
        Ncontentrows: dict = dict()
        AdapterContentrows: dict = dict()
        KMercontentrows: dict = dict()
        if basicstatistics & perbasegccontent & tilingrows & perbasesequencequality \
                & results_perbase_sequencecontentA & results_perbase_sequencecontentT \
                & results_perbase_sequencecontentG & results_perbase_sequencecontentC & Ncontentrows & \
                AdapterContentrows & KMercontentrows & perbasesequencecontentA & perbasesequencecontentT & \
                perbasesequencecontentG & perbasesequencecontentC & resultsdata:
            return basicstatistics, perbasegccontent, tilingrows, \
                   perbasesequencequality, results_perbase_sequencecontentA, results_perbase_sequencecontentT, \
                   results_perbase_sequencecontentG, results_perbase_sequencecontentC, Ncontentrows, \
                   AdapterContentrows, KMercontentrows, perbasesequencecontentA, perbasesequencecontentT, perbasesequencecontentG, \
                   perbasesequencecontentC, resultsdata
        else:
            raise Exception("Unable to initialize")

    except Exception as exception:
        print("Exception: %s" % exception)

    finally:
        print("Finished initializing")
