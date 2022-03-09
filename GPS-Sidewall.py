#!/usr/bin/env python
# coding: utf-8

# In[14]:


import re
from re import *
import os
import string
from itertools import *
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from PIL import ImageTk,Image 
import math
import numpy as np


# In[28]:


def make_xml():
    try:
        import tkinter as tk
        import pathlib
        import sys
        from tkinter import filedialog,messagebox
        from pathlib import os
        import os
        import re
        from re import split

        # Define Variables

        tire_name  = e1.get()
        tire_size  = e2.get()
        order_num  = e3.get()
        track = variable1.get()
        mod_seq = variable2.get()
        
        CAM_dir = '//global/americas/data/cam/CAM/GOODYEAR' 
        Machine = variable3.get()
        GPS_end = 'TREAD_SIDEWALL/documents/GPS'
        models_end = 'TREAD_SIDEWALL/models/HyperMill'

        # Define directory on the I-drive

        GPS_dir = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, GPS_end])
        models_dir = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, models_end])
        
        
        #### ERROR HANDLING #####

        # Check if Mold directory exists on I-drive
        if os.path.isdir(GPS_dir) ==  False:
            messagebox.showerror("Error", GPS_dir + ' does not exist')
            return 
        # Check if there is a sequence file in GPS folder
        if len(os.listdir(GPS_dir)) == 0:
            messagebox.showerror("Error", 'GPS folder is empty!')
            return
        # Check if there is more than one file in GPS folder
        if len(os.listdir(GPS_dir)) > 1:
            messagebox.showerror("Error", 'Too many files in GPS folder')
            return
        
        # Check if there are iges files on the I-drive
        if len(os.listdir(GPS_dir)) == 0:
            messagebox.showerror("Error", 'No iges files found!')
            return
        
        try: 
            start_pitch = int(e4.get())
        except:
            messagebox.showerror("Error", 'Input a valid integer for START PITCH')
            return
        try: 
            offsetAngle = float(e5.get())
        except:
            messagebox.showerror("Error", 'Input a valid value for OFFSET ANGLE')
            return
        
        
        #### END ERROR HANDLING
        
        
        
        
        # Open Seq File and read all lines to Variable A
        file = os.listdir(GPS_dir)[0]
        gy_pseq = '/'.join([GPS_dir, file])
        fid = open(gy_pseq, "r")
        Content = fid.read() 
        A = Content.split("\n")
        
        pitchNum = int(A[1].split(' ')[-1])
        
        if pitchNum != len(mod_seq):
            alphabet_string = string.ascii_uppercase
            order = ''.join([alphabet_string[i] for i in range(pitchNum)])
            messagebox.showerror("Error", "Model Sequnce should be: {0}".format(order))
            return

        # Getting Number of Pitch Models
        pitchModels = int(A[2].split(":")[0])

        # Getting Total pitches in Sequence
        pitchCount_index = pitchNum + 2
        pitchCount = int(A[pitchCount_index])
        
        # Create pitch ratio list
        pitchSplit = re.split(':|,|;| ', A[2])
        while True:
            try:
                pitchSplit.remove('')
            except:
                break
        last = len(pitchSplit)+1
        k = 0
        while len(pitchSplit) != pitchModels:
            pitchSplit.pop(k)
            k+=1
        
        
        # Creating list of pitch models as string
        pitchSize = list(range(1,pitchNum+1)) 
        for p in range(pitchNum):
            pitchSize[p] = str(pitchSize[p])
            
        pitchSize_mod = list(range(1,pitchNum+1)) 
        alphabet_string = string.ascii_uppercase
        for i in range(pitchNum):
            pitchSize_mod[i] = str(alphabet_string.index(mod_seq[i])+1)

        # Create List of all pitch combinations
        for i in range(pitchNum*pitchModels):
            Pitches = [[x,y] for x in pitchSplit for y in pitchSize]
        #Creating pitch sequence as a List

        pitchSequence = []
        for i in range(pitchCount_index+1,len(A)-1):
            line = A[i].split(' ')
            while True:
                try:
                    line.remove('')
                except:
                    break
            pitchSequence = pitchSequence + line

        # Removing spaces
        pitchSequence = [re.split(';|,', pitchSequence[i]) for i in range(len(pitchSequence))]
        for i in range(len(pitchSequence)):
            pitchSequence[i].remove('')
        # Fixing Spacing Issues
        count = 0
        while count < pitchCount:
            if len(pitchSequence[count])>2:
                com1 = [pitchSequence[count][0:2]]
                com2 = [pitchSequence[count][2::]]
                pitch_save_front = pitchSequence[0:count]
                pitch_save_end = pitchSequence[count+1::]
                pitchSequence = pitch_save_front + com1 +com2

                for seq in pitch_save_end:
                    pitchSequence.append(seq)

                count+=2
            else:
                count+=1
        
        # Convert Pitch sequence
        for p in range(len(pitchSequence)):
            index = int(pitchSequence[p][-1])
            new = pitchSize_mod[index-1]
            pitchSequence[p][-1] = new  
            
        
        # Create Goodyear Pitch Sequence
        GPS = []
        for i in range(pitchCount):
            for k in range(pitchNum*pitchModels):
                num = Pitches[k]
                if pitchSequence[i] == num:
                    GPS = GPS + [str(k+1)]
                    
                    
        #### Pitch angles and Shift angles ####
    
        if track == 'Bottom Sidewall':
            ops = '_Bot'
            track_path = 'BOTTOM SIDEWALL'
        if track == 'Top Sidewall':
            ops = '_Top'
            track_path = 'TOP SIDEWALL'
        
        models = os.listdir(models_dir)
        
        track_models = []
        for file in models:
            if search(ops,file):
                if search(' S ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' M ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' L ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' XL ',file):
                    track_models.append(file)
        
        

                 
        angles = []
        shift = []
        for i in range(len(track_models)):

            fname = track_models[i]
            fpath = models_dir + '/' + fname
            fid = open(fpath, "r")
            Counter = 0
            Content = fid.read() 
            A = Content.split("\n") 

            for i in A: 
                if i: 
                    Counter += 1
            fid.close()

            # Sort Data into Heading variable
            Heading = A[0:6]
            A = A[6:]

            count = 0
            for i in range(len(A)):
                seq_num = A[i][-8:]
                if seq_num[0] == 'D':
                    count += 1
                else:
                    break
            Data = A[0:count]
            A = A[count:]

            # Sort Data into Parameters variable
            Parameters = A[0:-1]
            A = []
            data_size = int(len(Data)/2)
            class structtype:
                pass
            data = [ structtype() for i in range(data_size)]

            for i in range(len(Data)):
                line = Data[i]
                check = i%2
                if check == 0:
                    index = int(i/2)
                    data[index].EntityTypeL1          = line[0:8]
                    data[index].PDPointer             = line[8:16]
                    data[index].Structure             = line[16:24]
                    data[index].LineFontPattern       = line[24:32]
                    data[index].Level                 = line[32:40]
                    data[index].View                  = line[40:48]
                    data[index].TransMatrix           = line[48:56]
                    data[index].LabelDispAssoc        = line[56:64]
                    data[index].StatusNum             = line[64:72]
                    data[index].SectionSequenceNumL1  = line[72:80]
                else:
                    index = int((i-1)/2)
                    data[index].EntityTypeL2          = line[0:8]
                    data[index].LineWeight            = line[8:16]
                    data[index].ColorNum              = line[16:24]           
                    data[index].ParameterLineCount    = line[24:32]
                    data[index].FormNum               = line[32:40]
                    data[index].Reserved              = line[40:56]
                    data[index].EntityLabel           = line[56:64]
                    data[index].EntitySubsriptNum     = line[64:72]
                    data[index].SectionSequenceNumL2  = line[72:80]

            POINT_code    = 116;     # Point
            count116=0

            for i in range(len(data)):
                if '00' in data[i].StatusNum[0:2]:
                    num_def = int(data[i].EntityTypeL1)
                    if num_def == POINT_code:
                        count116 += 1
                    else:
                        pass
            POINT_index    = [0]*count116
            count116=0

            for i in range(len(data)):
                if '00' in data[i].StatusNum[0:2]:
                    num_def = int(data[i].EntityTypeL1)
                    if num_def == POINT_code:
                        POINT_index[count116] = i
                        count116 += 1
                    else:
                        pass


            #Remove non colored points
            Arc_points = []

            for i in range(len(POINT_index)):
                color = int(data[POINT_index[i]].ColorNum)

                if color != 0:
                    Arc_points.append(POINT_index[i])     


            center_vector = [0,1]        

            cord = [[0,0],[0,0]]
            ARC = []

            for i in range(len(Arc_points)):
                k = Arc_points[i]
                index = int(data[k].PDPointer)-1
                param = Parameters[index].split(',')
                X = float(param[1])
                Z = float(param[3])
                cord[i][0] = X
                cord[i][1] = Z

            vector_1 = cord[0]
            vector_2 = cord[1]

            unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
            unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
            center_vector = [0,1]
            theta1 = np.arccos(np.dot(unit_vector_1, center_vector))*180/math.pi
            theta2 = np.arccos(np.dot(unit_vector_2, center_vector))*180/math.pi
            theta = [theta1,theta2]
            dot_product = np.dot(unit_vector_1, unit_vector_2)
            angles.append(np.arccos(dot_product)*180/math.pi)
            shift.append(max(theta) - 0.5*np.arccos(dot_product)*180/math.pi)
            
        # Calculate Angles Sequence
        Angle_seq = []
        for i in range(len(GPS)):
            p_spot = int(GPS[i])-1
            angle_val = angles[p_spot]
            Angle_seq.append(angle_val)
        
        # Calculate Start Angle
        start_index = start_pitch 
        start_angle = Angle_seq[0]/2
        
        for i in range(1,start_index):
            start_angle = start_angle+(Angle_seq[i])
        
        start_angle = (start_angle + offsetAngle)*-1
        
        
        
        #### Write the XML File ###
        path_part = 'TREAD_SIDEWALL\HyperMill'
        xml_name = 'tire.xml'
        xml_path =  '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, path_part, track_path, 'DEF', xml_name ])          
        
        f = open(xml_path, "w")
        
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')  
        f.write('<Project Customer="GOODYEAR" Name="{0} {1}" Image="">\n'.format(tire_size,order_num))
        f.write('	<Tire Name="" ProductionMode="Mold">\n')  
        f.write('		<ManufacturingContext SecurityRadius="30" CopyNCOutputMode="CopyNCOutputAll"/>\n')  
        f.write('		<SegmentSequence Orientation="Clockwise" S_Diameter="0" T_Diameter="1000" SegmentExtAngle="1" StockExtAngle="1" AutoOffsetAngle="0" StartOffsetAngle="0">\n')  
        for i in range(6):
            f.write('			<Segment ID="{0}" Angle="60" OffsetAngle="0" Name=""/>\n'.format(str(i+1)))
        f.write('		</SegmentSequence>\n')  
        f.write('		<Tracks>\n')  
        f.write('			<Track Name="1:Track" ID="1" SegmentGeneration="1">\n')  
        f.write('				<Pitches>\n')
        for i in range(pitchNum*pitchModels):
            f.write('					<Pitch Angle="{0}" Name="{1}:Pitch" ID="{1}"/>\n'.format(str(angles[i]),str(i+1))) 
        f.write('				</Pitches>\n')  
        f.write('				<AdjacentPitches>\n')  
        f.write('					<AdjacentPitch ID="1" Name="1:Adjacent pitch" Type="UsePitch" PitchID="1"/>\n') 
        f.write('				</AdjacentPitches>\n') 
        f.write('				<PitchSequence Orientation="Clockwise" StartAngle="{0}" CopyAngleMode="None">\n'.format(str(start_angle)))
        
        for i in range(len(GPS)):
            f.write('					<PitchPosition CopyMode="None" Angle="0" PitchID="{0}"/>\n'.format(GPS[i]))
        f.write('				</PitchSequence>\n')
        f.write('				<PitchCombinations/>\n') 
        f.write('				<PitchProgrammingCombinations>\n')
        for i in range(pitchNum*pitchModels):
            f.write('					<PitchProgrammingCombination PitchID="{0}" LeftAdjacentPitchID="1" RightAdjacentPitchID="1"/>\n'.format(str(i+1)))
        f.write('				</PitchProgrammingCombinations>\n')
        f.write('				<Feedback MarkerDistance="50"/>\n')
        f.write('			</Track>\n')
        f.write('		</Tracks>\n')
        f.write('		<Labels/>\n')
        f.write('	</Tire>\n')
        f.write('</Project>\n')
        
        f.close()

        messagebox.showinfo("Info Message", 'Success!: XML file generated')
        return
    except:
        messagebox.showerror("Error", 'Command Failed: Check values and try agian')
        return
        
    


# In[29]:


def make_csv():
    try:
        import tkinter as tk
        import pathlib
        import sys
        from tkinter import filedialog,messagebox
        from pathlib import os
        import pandas as pd
        import xlsxwriter
        import re

        # Define Variables
        tire_name  = e1.get()
        tire_size  = e2.get()
        order_num  = e3.get()
        track = variable1.get()
        mod_seq = variable2.get()
        
        CAM_dir = '//global/americas/data/cam/CAM/GOODYEAR' 
        Machine = variable3.get()
        GPS_end = 'TREAD_SIDEWALL/documents/GPS'
        models_end = 'TREAD_SIDEWALL/models/HyperMill'

        # Define directory on the I-drive

        GPS_dir = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, GPS_end])
        models_dir = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, models_end])
        
        
        #### ERROR HANDLING #####

        # Check if Mold directory exists on I-drive
        if os.path.isdir(GPS_dir) ==  False:
            messagebox.showerror("Error", GPS_dir + ' does not exist')
            return 
        # Check if there is a sequence file in GPS folder
        if len(os.listdir(GPS_dir)) == 0:
            messagebox.showerror("Error", 'GPS folder is empty!')
            return
        # Check if there is more than one file in GPS folder
        if len(os.listdir(GPS_dir)) > 1:
            messagebox.showerror("Error", 'Too many files in GPS folder')
            return
        
        # Check if there are iges files on the I-drive
        if len(os.listdir(GPS_dir)) == 0:
            messagebox.showerror("Error", 'No iges files found!')
            return
        
        try: 
            start_pitch = int(e4.get())
        except:
            messagebox.showerror("Error", 'Input a valid integer for START PITCH')
            return
        try: 
            offsetAngle = float(e5.get())
        except:
            messagebox.showerror("Error", 'Input a valid value for OFFSET ANGLE')
            return
        
        
        #### END ERROR HANDLING
        
        
        
        
        # Open Seq File and read all lines to Variable A
        file = os.listdir(GPS_dir)[0]
        gy_pseq = '/'.join([GPS_dir, file])
        fid = open(gy_pseq, "r")
        Content = fid.read() 
        A = Content.split("\n")
        
        pitchNum = int(A[1].split(' ')[-1])
        
        if pitchNum != len(mod_seq):
            alphabet_string = string.ascii_uppercase
            order = ''.join([alphabet_string[i] for i in range(pitchNum)])
            messagebox.showerror("Error", "Model Sequnce should be: {0}".format(order))
            return

        # Getting Number of Pitch Models
        pitchModels = int(A[2].split(":")[0])

        # Getting Total pitches in Sequence
        pitchCount_index = pitchNum + 2
        pitchCount = int(A[pitchCount_index])
        
        # Create pitch ratio list
        pitchSplit = re.split(':|,|;| ', A[2])
        while True:
            try:
                pitchSplit.remove('')
            except:
                break
        last = len(pitchSplit)+1
        k = 0
        while len(pitchSplit) != pitchModels:
            pitchSplit.pop(k)
            k+=1
        
        
        # Creating list of pitch models as string
        pitchSize = list(range(1,pitchNum+1)) 
        for p in range(pitchNum):
            pitchSize[p] = str(pitchSize[p])
            
        pitchSize_mod = list(range(1,pitchNum+1)) 
        alphabet_string = string.ascii_uppercase
        for i in range(pitchNum):
            pitchSize_mod[i] = str(alphabet_string.index(mod_seq[i])+1)

        # Create List of all pitch combinations
        for i in range(pitchNum*pitchModels):
            Pitches = [[x,y] for x in pitchSplit for y in pitchSize]
        #Creating pitch sequence as a List

        pitchSequence = []
        for i in range(pitchCount_index+1,len(A)-1):
            line = A[i].split(' ')
            while True:
                try:
                    line.remove('')
                except:
                    break
            pitchSequence = pitchSequence + line

        # Removing spaces
        pitchSequence = [re.split(';|,', pitchSequence[i]) for i in range(len(pitchSequence))]
        for i in range(len(pitchSequence)):
            pitchSequence[i].remove('')
        # Fixing Spacing Issues
        count = 0
        while count < pitchCount:
            if len(pitchSequence[count])>2:
                com1 = [pitchSequence[count][0:2]]
                com2 = [pitchSequence[count][2::]]
                pitch_save_front = pitchSequence[0:count]
                pitch_save_end = pitchSequence[count+1::]
                pitchSequence = pitch_save_front + com1 +com2

                for seq in pitch_save_end:
                    pitchSequence.append(seq)

                count+=2
            else:
                count+=1
        
        # Convert Pitch sequence
        for p in range(len(pitchSequence)):
            index = int(pitchSequence[p][-1])
            new = pitchSize_mod[index-1]
            pitchSequence[p][-1] = new  
            
        
        # Create Goodyear Pitch Sequence
        GPS = []
        for i in range(pitchCount):
            for k in range(pitchNum*pitchModels):
                num = Pitches[k]
                if pitchSequence[i] == num:
                    GPS = GPS + [str(k+1)]
                    
                    
        #### Pitch angles and Shift angles ####
    
        if track == 'Bottom Sidewall':
            ops = '_Bot'
            track_path = 'BOTTOM SIDEWALL'
        if track == 'Top Sidewall':
            ops = '_Top'
            track_path = 'TOP SIDEWALL'
        
        models = os.listdir(models_dir)
        
        track_models = []
        for file in models:
            if search(ops,file):
                if search(' S ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' M ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' L ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' XL ',file):
                    track_models.append(file)
        
        

                 
        angles = []
        shift = []
        for i in range(len(track_models)):

            fname = track_models[i]
            fpath = models_dir + '/' + fname
            fid = open(fpath, "r")
            Counter = 0
            Content = fid.read() 
            A = Content.split("\n") 

            for i in A: 
                if i: 
                    Counter += 1
            fid.close()

            # Sort Data into Heading variable
            Heading = A[0:6]
            A = A[6:]

            count = 0
            for i in range(len(A)):
                seq_num = A[i][-8:]
                if seq_num[0] == 'D':
                    count += 1
                else:
                    break
            Data = A[0:count]
            A = A[count:]

            # Sort Data into Parameters variable
            Parameters = A[0:-1]
            A = []
            data_size = int(len(Data)/2)
            class structtype:
                pass
            data = [ structtype() for i in range(data_size)]

            for i in range(len(Data)):
                line = Data[i]
                check = i%2
                if check == 0:
                    index = int(i/2)
                    data[index].EntityTypeL1          = line[0:8]
                    data[index].PDPointer             = line[8:16]
                    data[index].Structure             = line[16:24]
                    data[index].LineFontPattern       = line[24:32]
                    data[index].Level                 = line[32:40]
                    data[index].View                  = line[40:48]
                    data[index].TransMatrix           = line[48:56]
                    data[index].LabelDispAssoc        = line[56:64]
                    data[index].StatusNum             = line[64:72]
                    data[index].SectionSequenceNumL1  = line[72:80]
                else:
                    index = int((i-1)/2)
                    data[index].EntityTypeL2          = line[0:8]
                    data[index].LineWeight            = line[8:16]
                    data[index].ColorNum              = line[16:24]           
                    data[index].ParameterLineCount    = line[24:32]
                    data[index].FormNum               = line[32:40]
                    data[index].Reserved              = line[40:56]
                    data[index].EntityLabel           = line[56:64]
                    data[index].EntitySubsriptNum     = line[64:72]
                    data[index].SectionSequenceNumL2  = line[72:80]

            POINT_code    = 116;     # Point
            count116=0

            for i in range(len(data)):
                if '00' in data[i].StatusNum[0:2]:
                    num_def = int(data[i].EntityTypeL1)
                    if num_def == POINT_code:
                        count116 += 1
                    else:
                        pass
            POINT_index    = [0]*count116
            count116=0

            for i in range(len(data)):
                if '00' in data[i].StatusNum[0:2]:
                    num_def = int(data[i].EntityTypeL1)
                    if num_def == POINT_code:
                        POINT_index[count116] = i
                        count116 += 1
                    else:
                        pass


            #Remove non colored points
            Arc_points = []

            for i in range(len(POINT_index)):
                color = int(data[POINT_index[i]].ColorNum)

                if color != 0:
                    Arc_points.append(POINT_index[i])     


            center_vector = [0,1]        

            cord = [[0,0],[0,0]]
            ARC = []

            for i in range(len(Arc_points)):
                k = Arc_points[i]
                index = int(data[k].PDPointer)-1
                param = Parameters[index].split(',')
                X = float(param[1])
                Z = float(param[3])
                cord[i][0] = X
                cord[i][1] = Z

            vector_1 = cord[0]
            vector_2 = cord[1]

            unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
            unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
            center_vector = [0,1]
            theta1 = np.arccos(np.dot(unit_vector_1, center_vector))*180/math.pi
            theta2 = np.arccos(np.dot(unit_vector_2, center_vector))*180/math.pi
            theta = [theta1,theta2]
            dot_product = np.dot(unit_vector_1, unit_vector_2)
            angles.append(np.arccos(dot_product)*180/math.pi)
            shift.append(max(theta) - 0.5*np.arccos(dot_product)*180/math.pi)
            
        # Calculate Angles Sequence
        Angle_seq = []
        for i in range(len(GPS)):
            p_spot = int(GPS[i])-1
            angle_val = angles[p_spot]
            Angle_seq.append(angle_val)
        
        # Calculate Start Angle
        start_index = start_pitch
        start_angle = Angle_seq[0]/2
        
        for i in range(1,start_index):
            start_angle = start_angle+(Angle_seq[i])
        
        start_angle = (start_angle + offsetAngle)*-1
        
        
        
        #### Write the CSV File ###
        path_part = 'TREAD_SIDEWALL/HyperMill'
        csv_name = 'ANGLES.csv'
        xlsx_name = 'ANGLES.xlsx'
        csv_path =  '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, path_part, track_path, 'DOC', csv_name ])          
        xlsx_path = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, path_part, track_path, 'DOC', xlsx_name])
        workbook = xlsxwriter.Workbook(xlsx_path)
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Pitch Num')
        worksheet.write('B1', 'ARC')
        worksheet.write('C1', 'SHIFT')
        worksheet.write('D1', 'FILE NAME')
        for i in range(len(Pitches)):
            name = 'Pitch {0}'.format(str(i+1))
            worksheet.write(i+1,0,name)
            worksheet.write(i+1,1,angles[i])
            worksheet.write(i+1,2,shift[i])
            worksheet.write(i+1,3,track_models[i])    
        
        workbook.close()
        
        # Convert xlsx file to csv
        read_file = pd.read_excel(xlsx_path)
        read_file.to_csv(csv_path, index = None,header=True)
    
        
        messagebox.showinfo("Info Message", 'Success!: ANGLES files created')
        return
    except:
        messagebox.showerror("Error", 'Command Failed: Check values and try agian')
        return
    


# In[30]:


def make_pitch_seq():
    try:
        import tkinter as tk
        import pathlib
        import sys
        from tkinter import filedialog,messagebox
        from pathlib import os
        import pandas as pd
        import xlsxwriter
        import re

        # Define Variables
        tire_name  = e1.get()
        tire_size  = e2.get()
        order_num  = e3.get()
        track = variable1.get()
        mod_seq = variable2.get()
        
        CAM_dir = '//global/americas/data/cam/CAM/GOODYEAR'  
        Machine = variable3.get()
        GPS_end = 'TREAD_SIDEWALL/documents/GPS'
        models_end = 'TREAD_SIDEWALL/models/HyperMill'

        # Define directory on the I-drive

        GPS_dir = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, GPS_end])
        models_dir = '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, models_end])
        
        
        #### ERROR HANDLING #####

        # Check if Mold directory exists on I-drive
        if os.path.isdir(GPS_dir) ==  False:
            messagebox.showerror("Error", GPS_dir + ' does not exist')
            return 
        # Check if there is a sequence file in GPS folder
        if len(os.listdir(GPS_dir)) == 0:
            messagebox.showerror("Error", 'GPS folder is empty!')
            return
        # Check if there is more than one file in GPS folder
        if len(os.listdir(GPS_dir)) > 1:
            messagebox.showerror("Error", 'Too many files in GPS folder')
            return
        
        # Check if there are iges files on the I-drive
        if len(os.listdir(GPS_dir)) == 0:
            messagebox.showerror("Error", 'No iges files found!')
            return
        
        try: 
            start_pitch = int(e4.get())
        except:
            messagebox.showerror("Error", 'Input a valid integer for START PITCH')
            return
        try: 
            offsetAngle = float(e5.get())
        except:
            messagebox.showerror("Error", 'Input a valid value for OFFSET ANGLE')
            return
        
        
        #### END ERROR HANDLING
        
        
        
        
        # Open Seq File and read all lines to Variable A
        file = os.listdir(GPS_dir)[0]
        gy_pseq = '/'.join([GPS_dir, file])
        fid = open(gy_pseq, "r")
        Content = fid.read() 
        A = Content.split("\n")
        
        pitchNum = int(A[1].split(' ')[-1])
        
        if pitchNum != len(mod_seq):
            alphabet_string = string.ascii_uppercase
            order = ''.join([alphabet_string[i] for i in range(pitchNum)])
            messagebox.showerror("Error", "Model Sequnce should be: {0}".format(order))
            return

        # Getting Number of Pitch Models
        pitchModels = int(A[2].split(":")[0])

        # Getting Total pitches in Sequence
        pitchCount_index = pitchNum + 2
        pitchCount = int(A[pitchCount_index])
        
        # Create pitch ratio list
        pitchSplit = re.split(':|,|;| ', A[2])
        while True:
            try:
                pitchSplit.remove('')
            except:
                break
        last = len(pitchSplit)+1
        k = 0
        while len(pitchSplit) != pitchModels:
            pitchSplit.pop(k)
            k+=1
        
        
        # Creating list of pitch models as string
        pitchSize = list(range(1,pitchNum+1)) 
        for p in range(pitchNum):
            pitchSize[p] = str(pitchSize[p])
            
        pitchSize_mod = list(range(1,pitchNum+1)) 
        alphabet_string = string.ascii_uppercase
        for i in range(pitchNum):
            pitchSize_mod[i] = str(alphabet_string.index(mod_seq[i])+1)

        # Create List of all pitch combinations
        for i in range(pitchNum*pitchModels):
            Pitches = [[x,y] for x in pitchSplit for y in pitchSize]
        #Creating pitch sequence as a List

        pitchSequence = []
        for i in range(pitchCount_index+1,len(A)-1):
            line = A[i].split(' ')
            while True:
                try:
                    line.remove('')
                except:
                    break
            pitchSequence = pitchSequence + line

        # Removing spaces
        pitchSequence = [re.split(';|,', pitchSequence[i]) for i in range(len(pitchSequence))]
        for i in range(len(pitchSequence)):
            pitchSequence[i].remove('')
        # Fixing Spacing Issues
        count = 0
        while count < pitchCount:
            if len(pitchSequence[count])>2:
                com1 = [pitchSequence[count][0:2]]
                com2 = [pitchSequence[count][2::]]
                pitch_save_front = pitchSequence[0:count]
                pitch_save_end = pitchSequence[count+1::]
                pitchSequence = pitch_save_front + com1 +com2

                for seq in pitch_save_end:
                    pitchSequence.append(seq)

                count+=2
            else:
                count+=1
        
        # Convert Pitch sequence
        for p in range(len(pitchSequence)):
            index = int(pitchSequence[p][-1])
            new = pitchSize_mod[index-1]
            pitchSequence[p][-1] = new  
            
        
        # Create Goodyear Pitch Sequence
        GPS = []
        for i in range(pitchCount):
            for k in range(pitchNum*pitchModels):
                num = Pitches[k]
                if pitchSequence[i] == num:
                    GPS = GPS + [str(k+1)]
                    
                    
        #### Pitch angles and Shift angles ####
    
        if track == 'Bottom Sidewall':
            ops = '_Bot'
            track_path = 'BOTTOM SIDEWALL'
        if track == 'Top Sidewall':
            ops = '_Top'
            track_path = 'TOP SIDEWALL'
        
        models = os.listdir(models_dir)
        
        track_models = []
        for file in models:
            if search(ops,file):
                if search(' S ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' M ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' L ',file):
                    track_models.append(file)
        for file in models:
            if search(ops,file):
                if search(' XL ',file):
                    track_models.append(file)
        
        

                 
        angles = []
        shift = []
        for i in range(len(track_models)):

            fname = track_models[i]
            fpath = models_dir + '/' + fname
            fid = open(fpath, "r")
            Counter = 0
            Content = fid.read() 
            A = Content.split("\n") 

            for i in A: 
                if i: 
                    Counter += 1
            fid.close()

            # Sort Data into Heading variable
            Heading = A[0:6]
            A = A[6:]

            count = 0
            for i in range(len(A)):
                seq_num = A[i][-8:]
                if seq_num[0] == 'D':
                    count += 1
                else:
                    break
            Data = A[0:count]
            A = A[count:]

            # Sort Data into Parameters variable
            Parameters = A[0:-1]
            A = []
            data_size = int(len(Data)/2)
            class structtype:
                pass
            data = [ structtype() for i in range(data_size)]

            for i in range(len(Data)):
                line = Data[i]
                check = i%2
                if check == 0:
                    index = int(i/2)
                    data[index].EntityTypeL1          = line[0:8]
                    data[index].PDPointer             = line[8:16]
                    data[index].Structure             = line[16:24]
                    data[index].LineFontPattern       = line[24:32]
                    data[index].Level                 = line[32:40]
                    data[index].View                  = line[40:48]
                    data[index].TransMatrix           = line[48:56]
                    data[index].LabelDispAssoc        = line[56:64]
                    data[index].StatusNum             = line[64:72]
                    data[index].SectionSequenceNumL1  = line[72:80]
                else:
                    index = int((i-1)/2)
                    data[index].EntityTypeL2          = line[0:8]
                    data[index].LineWeight            = line[8:16]
                    data[index].ColorNum              = line[16:24]           
                    data[index].ParameterLineCount    = line[24:32]
                    data[index].FormNum               = line[32:40]
                    data[index].Reserved              = line[40:56]
                    data[index].EntityLabel           = line[56:64]
                    data[index].EntitySubsriptNum     = line[64:72]
                    data[index].SectionSequenceNumL2  = line[72:80]

            POINT_code    = 116;     # Point
            count116=0

            for i in range(len(data)):
                if '00' in data[i].StatusNum[0:2]:
                    num_def = int(data[i].EntityTypeL1)
                    if num_def == POINT_code:
                        count116 += 1
                    else:
                        pass
            POINT_index    = [0]*count116
            count116=0

            for i in range(len(data)):
                if '00' in data[i].StatusNum[0:2]:
                    num_def = int(data[i].EntityTypeL1)
                    if num_def == POINT_code:
                        POINT_index[count116] = i
                        count116 += 1
                    else:
                        pass


            #Remove non colored points
            Arc_points = []

            for i in range(len(POINT_index)):
                color = int(data[POINT_index[i]].ColorNum)

                if color != 0:
                    Arc_points.append(POINT_index[i])     


            center_vector = [0,1]        

            cord = [[0,0],[0,0]]
            ARC = []

            for i in range(len(Arc_points)):
                k = Arc_points[i]
                index = int(data[k].PDPointer)-1
                param = Parameters[index].split(',')
                X = float(param[1])
                Z = float(param[3])
                cord[i][0] = X
                cord[i][1] = Z

            vector_1 = cord[0]
            vector_2 = cord[1]

            unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
            unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
            center_vector = [0,1]
            theta1 = np.arccos(np.dot(unit_vector_1, center_vector))*180/math.pi
            theta2 = np.arccos(np.dot(unit_vector_2, center_vector))*180/math.pi
            theta = [theta1,theta2]
            dot_product = np.dot(unit_vector_1, unit_vector_2)
            angles.append(np.arccos(dot_product)*180/math.pi)
            shift.append(max(theta) - 0.5*np.arccos(dot_product)*180/math.pi)
            
        # Calculate Angles Sequence
        Angle_seq = []
        for i in range(len(GPS)):
            p_spot = int(GPS[i])-1
            angle_val = angles[p_spot]
            Angle_seq.append(angle_val)
        
        # Calculate Start Angle
        start_index = start_pitch
        start_angle = Angle_seq[0]/2
        
        for i in range(1,start_index):
            start_angle = start_angle+(Angle_seq[i])
        
        start_angle = (start_angle + offsetAngle)*-1
        
        
        
        #### Write the text file ###
        path_part = 'TREAD_SIDEWALL/HyperMill'
        Gps_name = 'PitchSeq.txt'
        seq_path =  '/'.join([CAM_dir, tire_name, tire_size, order_num, Machine, path_part, track_path, 'DOC', Gps_name])          
        sequence = ' '.join(GPS)
        
        f = open(seq_path, "w")
        f.write(sequence)
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('Start Angle:   {0}'.format(start_angle))
        
        f.close()

        messagebox.showinfo("Info Message", 'Success!: Pitch Sequence File Created')
        return
    except:
        messagebox.showerror("Error", 'Command Failed: Check values and try agian')
        return


# In[31]:


master = tk.Tk()
master.title('Goodyear Pitch Sequencer-Tread in Sidewall')
master.geometry("423x600")
master.configure(bg='blue')

p2 = [''.join(list(permutations('AB'))[i]) for i in range(len(list(permutations('AB'))))]
p3 = [''.join(list(permutations('ABC'))[i]) for i in range(len(list(permutations('ABC'))))]
p4 = [''.join(list(permutations('ABCD'))[i]) for i in range(len(list(permutations('ABCD'))))]
Mod = p2 + p3 + p4


# Display Gps Logo at top center of GUI
canvas = Canvas(master, width = 423, height = 201)  
canvas.grid(row = 0, column = 0, columnspan = 6)  
img = ImageTk.PhotoImage(Image.open("//global/americas/data/cam/CAM/OpenMind/Executables/PitchSequence/GPS/gps_logo.png"))  
canvas.create_image(0, 0, anchor=NW, image=img)  

tk.Label(master, text="TIRE NAME", fg='white', bg = 'blue').grid(row=1, sticky = "W")
tk.Label(master, text="TIRE SIZE", fg='white', bg = 'blue').grid(row=3, sticky = "W")
tk.Label(master, text="ORDER NUMBER", fg='white', bg = 'blue').grid(row=5, sticky = "W")
tk.Label(master, text="START PITCH", fg='white', bg = 'blue').grid(row=7, sticky = "W")
tk.Label(master, text="OFFSET ANGLE", fg='white', bg = 'blue').grid(row=9, sticky = "W")
tk.Label(master, text="TRACK", fg='white', bg = 'blue').grid(row=1, column = 4, sticky = "W")
tk.Label(master, text="MODEL SEQUENCE", fg='white', bg = 'blue').grid(row=3, column = 4, sticky = "W")
tk.Label(master, text="MACHINE", fg='white', bg = 'blue').grid(row=5, column = 4, sticky = "W")
tk.Label(master, text="               ",bg = 'blue').grid(row=10, sticky = "W")
tk.Label(master, text="               ",bg = 'blue').grid(row=11, sticky = "W")
tk.Label(master, text="               ",bg = 'blue').grid(row=12, sticky = "W")
tk.Label(master, text="               ",bg = 'blue').grid(row=13, sticky = "W")


e1 = tk.Entry(master)   #TIRE NAME
e2 = tk.Entry(master)   #TIRE SIZE
e3 = tk.Entry(master)   #ORDER NUMBER
e4 = tk.Entry(master)   #Start Pitch    
e5 = tk.Entry(master)   #Offset Angle


e1.grid(row=2, column=0, columnspan = 3, sticky = "EW") #TIRE NAME INPUT
e2.grid(row=4, column=0, sticky = "W") #TIRE SIZE INPUT
e3.grid(row=6, column=0, sticky = "W") #ORDER NUMBER INPUT
e4.grid(row=8, column=0, sticky = "W") #Start Pitch INPUT
e5.grid(row=10, column=0, sticky = "W") #Offset Angle INPUT



# Drop down menu for Selecting Track
options = ['Bottom Sidewall', 'Top Sidewall']
variable1 = tk.StringVar(master)
variable1.set(options[0])

opt1 = tk.OptionMenu(master, variable1, *options)
opt1.config(bg = 'white')
opt1.grid(row=2, column = 4, sticky = "W")


# Drop down menu for Sequence
variable2 = tk.StringVar(master)
variable2.set(Mod[0])

opt2 = tk.OptionMenu(master, variable2, *Mod)
opt2.config(bg = 'white')
opt2.grid(row=4, column = 4, sticky = "W")

# Drop down menu for Machine
options3 = ['HAAS', 'STINGER']
variable3 = tk.StringVar(master)
variable3.set(options3[0])

opt3 = tk.OptionMenu(master, variable3, *options3)
opt3.config(bg = 'white')
opt3.grid(row=6, column = 4, sticky = "W")






tk.Button(master, text='Create tire.XML', command=make_xml).grid(row=14, column=0, sticky='W')
tk.Button(master, text='Create ANGLES files', command=make_csv).grid(row=14, column=2, sticky = 'W')
tk.Button(master, text='Create PitchSequence.txt', command=make_pitch_seq).grid(row=14, column=4, sticky='E')

# a button widget which will open a 
# new window on button click
"""
btn = Button(master, 
             text ="Click to open Balloon Reference", 
             command = openNewWindow)
btn.grid(row=10, column=1)




"""
master.mainloop()


# In[ ]:




