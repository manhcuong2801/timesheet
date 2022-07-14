# Pre-requisite - Import the DictWriter class from csv  module
from csv import DictWriter

# The list of column names as mentioned in the CSV file
headersCSV = ["ID", "NAME", "SUBJECT"]
# The data assigned to the dictionary
dict = {"ID": "04", "NAME": "John", "SUBJECT": "Mathematics"}

# Pre-requisite - The CSV file should be manually closed before running this code.

# First, open the old CSV file in append mode, hence mentioned as 'a'
# Then, for the CSV file, create a file object
with open("BCC.csv", "a", newline="") as f_object:
    # Pass the CSV  file object to the Dictwriter() function
    # Result - a DictWriter object
    dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
    # Pass the data in the dictionary as an argument into the writerow() function
    dictwriter_object.writerow(dict)
    # Close the file object
    # f_object.close()
