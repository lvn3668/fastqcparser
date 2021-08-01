# Author: Lalitha Viswanathan
# Affiliation: Stanford Health Care
from typing import TextIO


def perseqqualityscores(filepointer: TextIO, line: str, resultsdata: dict, basequalityrows: list[str]) -> \
        tuple[TextIO, dict, list[str]]:
    """

    :param filepointer:
    :param line:
    :param resultsdata:
    :param basequalityrows:
    :return:
    """
    try:
        if line.startswith('>>Per sequence quality scores'):
            resultsdata['per_sequence_quality_scores'] = {}
            resultsdata['per_sequence_quality_scores']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['per_sequence_quality_scores']['perseqqualityrows'] = []
            basequalityrows: list[str] = resultsdata['per_sequence_quality_scores']['perseqqualityrows']

            # Get header row
            resultsdata['per_sequence_quality_scores']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows
            nextrow = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                basequalityrows.append(nextrow.rstrip().split('\t'))
                nextrow = filepointer.readline()
                vals: list[str] = nextrow.strip().split('\t')
                continue
            if basequalityrows:
                return filepointer, resultsdata, basequalityrows
            else:
                raise Exception("Base quality rows null")
    except Exception as exception:
        print("Error encountered extracting per sequence quality scores %s" % exception)
    finally:
        print("Finished extracting per sequence quality scores")
