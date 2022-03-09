import sys
import pandas as pd
import os
args = sys.argv
folder = args[1]
file = args[2]
folder = folder.split('\\')
folder = "/".join(folder)
excel_name = file[0:18] + '.xlsx'

read_file = pd.read_csv (folder + '/' + file)
read_file.to_excel (folder + '/' + excel_name, index = None, header=True)
