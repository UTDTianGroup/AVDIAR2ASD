import csv

def read_all_rows(csv_file_path, delimiter=','):
    with open(csv_file_path, 'r') as csvfile:
        csvfilereader = csv.reader(csvfile, delimiter=delimiter)
        all_rows = list(csvfilereader)
    return all_rows

def write_all_rows(csv_file_path, rows_to_write, header=None):
    
    with open(csv_file_path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        if header is not None:
            csvwriter.writerow(header)
        
        for row in rows_to_write:
            csvwriter.writerow(row)
        
        csvfile.flush()