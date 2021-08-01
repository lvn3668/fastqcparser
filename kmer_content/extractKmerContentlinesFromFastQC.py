# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare
# Package to extract KMer Content from FastQC
from typing import TextIO


def extractKMerContentLines(filepointer: TextIO, line: str, resultsdata: dict, KmerContentrows: list[str]) -> tuple[
    TextIO, dict, list[str]]:
    """

    :param resultsdata:
    :param filepointer:
    :param KmerContentrows:
    :type line: object
    """
    try:
        if line & line.startswith('>>Kmer Content') & resultsdata:
            resultsdata['KmerContent'] = {}
            resultsdata['KmerContent']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['KmerContent']['KmerContentrows'] = []
            KmerContentrows = resultsdata['KmerContent']['KmerContentrows']

            # Get header row
            resultsdata['KmerContent']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows
            nextrow = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                KmerContentrows.append(nextrow.rstrip().split('\t'))
                nextrow = filepointer.readline()
                continue
        else:
            raise Exception("Input parameters are null")
        if KmerContentrows:
            return filepointer, resultsdata, KmerContentrows
    except Exception as exception:
        print("Extracting KMer Content rows failed %s" % exception)
    finally:
        print("Extracting KMer Content rows succeeded")
