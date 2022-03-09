import sys
import shutil
import time
import os



args = sys.argv
folders = args[-1].split('\\')
user_name = folders[-1]
USERS_path = 'C:/Users/Public/Documents/OPEN MIND/USERS/'
tmp_ = 'C:/Users/Public/Documents/OPEN MIND/tmp'

## Delete Temp Files
dir_ = tmp_
print('Deleting files from tmp folder')
for file in os.scandir(dir_):
    try:
        os.remove(file.path)
    except:
        pass

## Delete the variants Folder
print('Deleting Variants folder')
dir_ = USERS_path + user_name + '/AutomationCenter/variants'
shutil.rmtree(dir_)

## Delete Programming Wizard Folder
print('Deleteing ProgrammingWizard Folder')
dir_ = USERS_path + 'API/ProgrammingWizard'
shutil.rmtree(dir_)

## Copy ProgrammingWizard Folder from Network Drive
print('Copying ProgrammingWizard Folder')

source_dir = r"\\global\americas\data\cam\CAM\OpenMind\Runtime Scripts\ProgrammingWizard"
destination_dir = USERS_path + 'API/ProgrammingWizard'
shutil.copytree(source_dir, destination_dir)
      
print('Finish...Closing in 3 seconds')

time.sleep(3)















