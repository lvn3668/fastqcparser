# Author: Lalitha Viswanathan
# Affiliation: Stanford Health Care
def extract_pertile_sequence_quality_records_from_FastQC(filepointer, line: str, resultsdata: dict,
                                                         tilingrows: dict):
    try:
        if line.startswith('>>Per tile sequence quality'):
            resultsdata['pertilesequencequality'] = {}
            resultsdata['pertilesequencequality']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['pertilesequencequality']['pertileseqqualityrows'] = []
            tilingrows = resultsdata['pertilesequencequality']['pertileseqqualityrows']

            # Get header row
            resultsdata['pertilesequencequality']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows
            nextrow = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                tilingrows.append(nextrow.rstrip().split('\t'))
                nextrow = filepointer.readline()
                continue
            if tilingrows:
                return filepointer, resultsdata, tilingrows
            else:
                raise Exception("Tiling rows information is null")
    except Exception as exception:
        print("Error encountered while extracting tile sequence quality information from FastQC %s " % exception)
    finally:
        print("Finished extracting tiling sequence information from FastQC file")
