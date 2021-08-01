# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare
# Get per base N Content
from typing import TextIO


def getperbaseNContent(filepointer: TextIO, line: str, resultsdata: dict, Ncontentrows: list[str]) -> tuple[
    TextIO, dict, list[str]]:
    """

    :param Ncontentrows:
    :param filepointer:
    :param line:
    :param resultsdata:
    :return:
    """
    try:
        if filepointer & line & line.startswith('>>Per base N content') & resultsdata:
            resultsdata['per_base_NContent'] = {}
            resultsdata['per_base_NContent']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['per_base_NContent']['perbaseNcontentrows'] = []
            Ncontentrows: list[str] = resultsdata['per_base_NContent']['perbaseNcontentrows']

            # Get header row
            resultsdata['per_base_NContent']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows
            nextrow: list[str] = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                Ncontentrows.append(nextrow.rstrip().split('\t'))
                nextrow = filepointer.readline()
                continue
        if Ncontentrows:
            return filepointer, resultsdata, Ncontentrows
        else:
            raise Exception("NContent rows null")
    except Exception as exception:
        print("Error in extracting N Content lines %s" % exception)
    finally:
        print("N Content lines parsed successfully")
