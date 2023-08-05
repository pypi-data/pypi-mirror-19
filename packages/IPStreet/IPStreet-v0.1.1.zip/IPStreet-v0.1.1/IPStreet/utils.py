import csv


def results_to_csv(response,target_file_path):
    """converts a response object to a csv"""
    keys = response[0].keys()

    try:
        output_file = open(target_file_path, 'w')
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(response)
    except OSError:
        print("Your target file path is invalid, it must be a .csv file")
