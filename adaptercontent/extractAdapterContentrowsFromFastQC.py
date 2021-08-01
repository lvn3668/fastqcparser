# Author: Lalitha Viswanathan
# Affiliation: Stanford HealthCare
def extractAdapterContentrows(filepointer: object, line: str, resultsdata: dict, AdapterContentrows: list[str]) -> object:
    """

    :type AdapterContentrows: list[str]
    :param contentrows:
    :rtype: object
    :param line: 
    :param resultsdata: 
    :return: 
    :type filepointer: object
    """
    try:
        if filepointer & line.startswith('>>Adapter Content') & line & resultsdata:

            resultsdata['AdapterContent'] = {}
            resultsdata['AdapterContent']['passfail'] = line.rstrip().split('\t')[1]
            resultsdata['AdapterContent']['AdapterContentrows'] = []
            AdapterContentrows = resultsdata['AdapterContent']['AdapterContentrows']

            # Get header row
            resultsdata['AdapterContent']['header'] = filepointer.readline().rstrip().split('\t')

            # Get other rows
            nextrow = filepointer.readline()
            while not nextrow.startswith('>>END_MODULE'):
                AdapterContentrows.append(nextrow.rstrip().split('\t'))
                nextrow = filepointer.readline()
                continue
        else:
            raise Exception("Input parameters null")
        if AdapterContentrows:
            return resultsdata, AdapterContentrows
        else:
            raise Exception("Adapter Content Rows null")
    except Exception as exception:
        print("Exception encountered while parsing adapter content rows %s " % exception)
    finally:
        print("Adapter content rows parsed successfully")
