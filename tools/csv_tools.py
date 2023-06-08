import csv

def read_all_rows(csv_file_path, delimiter=','):
    with open(csv_file_path, 'r') as csvfile:
        csvfilereader = csv.reader(csvfile, delimiter=delimiter)
        all_rows = list(csvfilereader)
    return all_rows