import os,csv


class CreateCSV:
    def __init__(self,csv_filepath:str='',dictionary:dict={}):

        if os.path.exists(csv_filepath):
            append_mode = 'a'  # File exists, open in append mode
        else:
            append_mode = 'w'  # File doesn't exist, open in write mode

        # Extract the header from the keys of the first dictionary
        header = dictionary.keys()

        # Append or create the CSV file and write the data
        with open(csv_filepath, mode=append_mode, newline='') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            if append_mode == 'w':
                writer.writeheader()  # Write the header if the file is created
            writer.writerow(dictionary)# Append dict as row
