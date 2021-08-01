# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare
# Utility to extract "Basic Statistics" lines from FastQC output file
from typing import TextIO


def extractBasicStatisticsLinesFromFastQC(filepointer: TextIO, line: str, resultsdata: dict,
                                          basicstatisticsdata: dict) -> tuple[TextIO, dict, dict]:
    """

    :type filepointer: TextIO
    :param filepointer:
    :type line: object
    :type basicstatisticsdata: object
    :type resultsdata: object
    """
    try:
        if filepointer & line & line.startswith('>>Basic Statistics') & resultsdata:
            resultsdata['basicstatistics'] = {}
            resultsdata['basicstatistics']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['basicstatistics']['basicstatisticsdata'] = {}
            basicstatisticsdata = resultsdata['basicstatistics']['basicstatisticsdata']

            # Skip line with "Measure  Value" labels
            nextrow = filepointer.readline()
            if nextrow.startswith('#Measure'):
                nextrow = filepointer.readline()

            while not nextrow.startswith('>>END_MODULE'):
                parts = nextrow.rstrip().split('\t')
                key = parts[0]
                value = parts[1]
                basicstatisticsdata[key] = value
                nextrow = filepointer.readline()
                continue
        else:
            raise Exception("Input parameters null")

        if basicstatisticsdata:
            return filepointer, resultsdata, basicstatisticsdata

    except Exception as exception:
        print("Error encountered parsing 'Basic Statistics' from FASTQC file %s" % exception)
    finally:
        print("Finished parsing 'Basic Statistics' portion from FastQC file")
