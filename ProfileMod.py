import tkinter as tk
import pathlib
import sys
from tkinter import filedialog,messagebox
from pathlib import os
root = tk.Tk()
root.withdraw()

file = filedialog.askopenfiles(initialdir = 'C:/',title='Select Profile Iges',filetypes=[('IGES Files', '.igs')])
if file is None:  # askopenfile() returns `None` if dialog closed with "cancel".  
    messagebox.showerror("Error", "No file selected")
    sys.exit()
for k in range(len(file)):
    dir_ = os.path.dirname(file[k].name)
    filetype = os.path.splitext(file[k].name)
    filetype = filetype[-1]
    new_dir = dir_ + '/Profile'
    os.chdir(dir_)
    if os.path.exists(new_dir):
        pass
    else:
        os.mkdir(new_dir)

    fname = file[k].name.replace(dir_ + '/','')
    fid = open(fname, "r")

    Counter = 0
    Content = fid.read() 
    A = Content.split("\n") 

    for i in A: 
        if i: 
            Counter += 1
    fid.close()

    # Sort Data into Heading variable
    Heading = A[0:5]
    A = A[5:]
    # Sort Data into Data variable
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

    # Data Entry Section 
    # Here we will organize the data entry section into a strucure array data 
    # with 19 fields (20 are given but the reserved field is repeated and is not
    # necessary to store as two seperate fields)
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
    # Sorting data.EntityTypeL1 into indivual matrices. These will serve as
    # the entity index values when performing calculations on parameter values.

    # Declaring entity type search variables
    ARC_code      = 100;     # Circular Arc
    CCURVE_code   = 102;     # Composite Curve
    LINE_code     = 110;     # Line 
    POINT_code    = 116;     # Point
    SREV_code     = 120;     # Surface of Revolution
    TCYL_code     = 122;     # Tabulated Cylinder
    XFORM_code    = 124;     # Transformation Matrix
    B_SPLINE_code = 126;     # Rational B-Spline Curve
    SPLSRF_code   = 128;     # Rational B-Spline Surface
    UV_BND_code   = 142;     # Curve on Parametric Surface
    TRM_SRF_code  = 144;     # Trimmed Surface
    COLOR_code    = 314;     # Color Definition
    LAYER_code    = 402;     # Associativity Instance
    PROP_code     = 406;     # Property
    # Counting entity types so that variables can be preallocated.
    count100=0;count102=0;count110=0;count116=0;count120=0;count122=0;count124=0;
    count126=0;count128=0;count142=0;count144=0;count314=0;count402=0;count406=0;
    for i in range(len(data)):
        if '00' in data[i].StatusNum[0:2]:
            num_def = int(data[i].EntityTypeL1)
            if num_def == ARC_code:
                count100 += 1
            elif num_def == CCURVE_code:
                count102 += 1
            elif num_def == LINE_code:
                count110 += 1
            elif num_def == POINT_code:
                count116 += 1
            elif num_def == SREV_code:
                count120 += 1
            elif num_def == TCYL_code:
                count122 += 1
            elif num_def == XFORM_code:
                count124 += 1
            elif num_def == B_SPLINE_code:
                count126 += 1
            elif num_def == SPLSRF_code:
                count128 += 1
            elif num_def == UV_BND_code:
                count142 += 1
            elif num_def == TRM_SRF_code:
                count144 += 1
            elif num_def == COLOR_code:
                count314 += 1
            elif num_def == LAYER_code:
                count402 += 1
            elif num_def == PROP_code:
                count406 += 1
            else:
                pass
    # Preallocate entity matrices
    ARC_index      = [0]*count100     # Circular Arc
    CCURVE_index   = [0]*count102     # Composite Curve
    LINE_index     = [0]*count110     # Line
    POINT_index    = [0]*count116     # Point
    SREV_index     = [0]*count120     # Surface of Revolution
    TCYL_index     = [0]*count122     # Tabulated Cylinder
    XFORM_index    = [0]*count124     # Transformation Matrix
    B_SPLINE_index = [0]*count126     # Rational B-Spline Curve
    SPLSRF_index   = [0]*count128     # Rational B-Spline Surface
    UV_BND_index   = [0]*count142     # Curve on Parametric Surface
    TRM_SRF_index  = [0]*count144     # Trimmed Surface
    COLOR_index    = [0]*count314     # Color Definition
    LAYER_index    = [0]*count402     # Associativity Instance
    PROP_index     = [0]*count406     # Property
    # Counting entity types that are visible and indexing to data structure
    count100=0;count102=0;count110=0;count116=0;count120=0;count122=0;count124=0;
    count126=0;count128=0;count142=0;count144=0;count314=0;count402=0;count406=0;
    for i in range(len(data)):
        if '00' in data[i].StatusNum[0:2]:
            num_def = int(data[i].EntityTypeL1)
            if num_def == ARC_code:
                ARC_index[count100] = i
                count100 += 1
            elif num_def == CCURVE_code:
                CCURVE_index[count102] = i
                count102 += 1
            elif num_def == LINE_code:
                LINE_index[count110] = i
                count110 += 1
            elif num_def == POINT_code:
                POINT_index[count116] = i
                count116 += 1
            elif num_def == SREV_code:
                SREV_index[count120] = i
                count120 += 1
            elif num_def == TCYL_code:
                TCYL_index[count122] = i
                count122 += 1
            elif num_def == XFORM_code:
                XFORM_index[count124] = i
                count124 += 1
            elif num_def == B_SPLINE_code:
                B_SPLINE_index[count126] = i
                count126 += 1
            elif num_def == SPLSRF_code:
                SPLSRF_index[count128] = i
                count128 += 1
            elif num_def == UV_BND_code:
                UV_BND_index[count142] = i
                count142 += 1
            elif num_def == TRM_SRF_code:
                TRM_SRF_index[count144] = i
                count144 += 1
            elif num_def == COLOR_code:
                COLOR_index[count314] = i
                count314 += 1
            elif num_def == LAYER_code:
                LAYER_index[count402] = i
                count402 += 1
            elif num_def == PROP_code:
                PROP_index[count406] = i
                count406 += 1
            else:
                pass
    # Determine CurveID pattern and layer/color curves
    Total_Curves = count100 + count110 + count126
    Curve_index = ARC_index+LINE_index+B_SPLINE_index
    Curve_index.sort()

    # Curve Pattern A - 42 total curves in profile iges
    if Total_Curves == 42 and count100 == 10:
        pat = 'A'
        NS = [5,6,7,19,20,21] 
        NS_RAD = [9,22]
        RSF = [4,40,1,18,41,15] 
        RSF_RAD = [8,14]
        RSF_TAN = [2,3,16,17]
        NS_count = 2
        RSF_count = 2
        RSF_TAN_count = 2
        NS_RAD_count = 4
        RSF_RAD_count = 4
        
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    
    # Curve Pattern B - 44 total curves in profile iges
    if Total_Curves == 44 and count100 == 12:
        pat = 'B'
        NS = [5,6,7,19,20,21] 
        NS_RAD = [9,22]
        RSF = [4,42,1,18,43,15] 
        RSF_RAD = [8,14]
        RSF_TAN = [2,3,16,17]
        NS_count = 2
        RSF_count = 2
        RSF_TAN_count = 2
        NS_RAD_count = 4
        RSF_RAD_count = 4
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    
    # Curve Pattern C - 46 total curves in profile iges
    if Total_Curves == 46 and count100 == 12:
        pat = 'C'
        NS = [28,29,30,40,41,42] 
        NS_RAD = [27,45]
        RSF = [23,43,20,39,36,44] 
        RSF_RAD = [17,33]
        RSF_TAN = [21,22,37,38]
        BUT_ARC = [19,35]
        BUT_FLT = [18,34]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 2
        RSF_RAD_count = 4
        RSF_TAN_count = 2
        BUT_ARC_count = 4
        BUT_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            elif i in BUT_ARC:
                data[Curve_index[i]].ColorNum = '       ' + str(BUT_ARC_count)
                data[Curve_index[i]].Level    = '     106'
                BUT_ARC_count += 1
            elif i in BUT_FLT:
                data[Curve_index[i]].ColorNum =  '       ' + str(BUT_FLT_count)
                data[Curve_index[i]].Level    = '     107'
                BUT_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
                
    # Curve Pattern D - 43 total curves in profile iges
    if Total_Curves == 43 and count100 == 12:
        pat = 'D'
        NS = [5,4,3,14,15,16] 
        NS_RAD = [2,13]
        RSF = [9,40,6,21,41,18] 
        RSF_RAD = [10,42]
        RSF_TAN = [7,8,19,20]
        NS_FLT = [1,12]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 2
        RSF_RAD_count = 4
        RSF_TAN_count = 2
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
                
    # Curve Pattern E - 41 total curves in profile iges
    if Total_Curves == 41 and count100 == 10:
        pat = 'E'
        NS = [19,20,21,30,31,32] 
        NS_RAD = [18,29]
        RSF = [25,38,22,37,39,34] 
        RSF_RAD = [26,40]
        RSF_TAN = [23,24,35,36]
        NS_FLT = [17,28]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 2
        RSF_RAD_count = 4
        RSF_TAN_count = 2
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
            
    # Curve Pattern F - 39 total curves in profile iges
    if Total_Curves == 39 and count100 == 8:
        pat = 'F'
        NS = [17,18,19,28,29,30] 
        NS_RAD = [16,27]
        RSF = [23,36,20,35,37,32] 
        RSF_RAD = [24,38]
        RSF_TAN = [21,22,33,34]
        NS_FLT = [15,26]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 2
        RSF_RAD_count = 4
        RSF_TAN_count = 2
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    # Curve Pattern G - 62 total curves in profile iges
    if Total_Curves == 62 and count100 == 22:
        pat = 'G'
        NS = [5,6,7,19,20,21] 
        NS_RAD = [9,22]
        RSF = [4,60,1,18,61,15] 
        RSF_RAD = [8,14]
        RSF_TAN = [2,3,16,17]
        NS_count = 2
        RSF_count = 2
        RSF_TAN_count = 2
        NS_RAD_count = 4
        RSF_RAD_count = 4
        
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]

    # Curve Pattern H - 55 total curves in profile iges
    if Total_Curves == 55 and count100 == 16:
        pat = 'H'
        NS = [19,20,21,30,31,32] 
        NS_RAD = [18,29]
        RSF = [25,52,22,37,53,34] 
        RSF_RAD = [26,54]
        RSF_TAN = [23,24,35,36]
        NS_FLT = [17,28]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 2
        RSF_RAD_count = 4
        RSF_TAN_count = 2
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    # Curve Pattern I - 61 total curves in profile iges
    if Total_Curves == 61 and count100 == 22:
        pat = 'I'
        NS = [5,4,3,14,15,16] 
        NS_RAD = [2,13]
        RSF = [9,58,6,21,59,18] 
        RSF_RAD = [10,60]
        RSF_TAN = [7,8,19,20]
        NS_FLT = [1,12]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 2
        RSF_RAD_count = 4
        RSF_TAN_count = 2
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in RSF_TAN:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_TAN_count)
                data[Curve_index[i]].Level    = '     105'
                RSF_TAN_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    # Curve Pattern AA - 44 total curves in profile iges
    if Total_Curves == 44 and count100 == 8:
        pat = 'AA'
        NS = [5,6,7,21,22,23] 
        NS_RAD = [9,24]
        RSF = [4,1,2,3,20,17,18,19] 
        RSF_RAD = [8,16]
        NS_count = 2
        RSF_count = 1
        NS_RAD_count = 4
        RSF_RAD_count = 4
        
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    
    # Curve Pattern BB - 46 total curves in profile iges
    if Total_Curves == 46 and count100 == 10:
        pat = 'BB'
        NS = [5,6,7,21,22,23] 
        NS_RAD = [9,24]
        RSF = [4,1,2,3,20,17,18,19] 
        RSF_RAD = [8,16]
        NS_count = 2
        RSF_count = 1
        NS_RAD_count = 4
        RSF_RAD_count = 4
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    
    # Curve Pattern CC - 48 total curves in profile iges
    if Total_Curves == 48 and count100 == 10:
        pat = 'CC'
        NS = [34,33,32,44,45,46] 
        NS_RAD = [31,47]
        RSF = [27,24,0,1,43,40,2,3] 
        RSF_RAD = [21,37]
        BUT_ARC = [23,39]
        BUT_FLT = [22,38]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 1
        RSF_RAD_count = 4
        BUT_ARC_count = 4
        BUT_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in BUT_ARC:
                data[Curve_index[i]].ColorNum = '       ' + str(BUT_ARC_count)
                data[Curve_index[i]].Level    = '     106'
                BUT_ARC_count += 1
            elif i in BUT_FLT:
                data[Curve_index[i]].ColorNum =  '       ' + str(BUT_FLT_count)
                data[Curve_index[i]].Level    = '     107'
                BUT_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
                
    # Curve Pattern DD - 45 total curves in profile iges
    if Total_Curves == 45 and count100 == 10:
        pat = 'DD'
        NS = [9,8,7,20,19,18] 
        NS_RAD = [6,17]
        RSF = [13,10,0,1,25,22,2,3] 
        RSF_RAD = [14,44]
        NS_FLT = [5,16]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 1
        RSF_RAD_count = 4
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
                
    # Curve Pattern EE - 43 total curves in profile iges
    if Total_Curves == 43 and count100 == 8:
        pat = 'EE'
        NS = [23,24,25,34,35,36] 
        NS_RAD = [22,33]
        RSF = [29,26,0,1,2,3,41,38] 
        RSF_RAD = [30,42]
        NS_FLT = [21,32]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 1
        RSF_RAD_count = 4
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
            
    # Curve Pattern FF - 41 total curves in profile iges
    if Total_Curves == 41 and count100 == 6:
        pat = 'FF'
        NS = [21,22,23,32,33,34] 
        NS_RAD = [20,31]
        RSF = [27,24,0,1,2,3,39,36] 
        RSF_RAD = [28,40]
        NS_FLT = [19,30]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 1
        RSF_RAD_count = 4
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    # Curve Pattern GG - 64 total curves in profile iges
    if Total_Curves == 64 and count100 == 20:
        pat = 'GG'
        NS = [5,6,7,21,22,23] 
        NS_RAD = [9,24]
        RSF = [1,2,3,4,17,18,19,20] 
        RSF_RAD = [8,16]
        NS_count = 2
        RSF_count = 1
        RSF_TAN_count = 2
        NS_RAD_count = 4
        RSF_RAD_count = 4
        
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]

    # Curve Pattern HH - 57 total curves in profile iges
    if Total_Curves == 57 and count100 == 14:
        pat = 'HH'
        NS = [23,24,25,34,35,36] 
        NS_RAD = [22,33]
        RSF = [29,26,0,1,2,3,38,41] 
        RSF_RAD = [30,56]
        NS_FLT = [21,32]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 1
        RSF_RAD_count = 4
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
    # Curve Pattern II - 63 total curves in profile iges
    if Total_Curves == 63 and count100 == 20:
        pat = 'II'
        NS = [9,8,7,20,19,18] 
        NS_RAD = [6,17]
        RSF = [13,10,0,1,25,22,2,3] 
        RSF_RAD = [14,62]
        NS_FLT = [5,16]
        NS_count = 2
        NS_RAD_count = 4
        RSF_count = 1
        RSF_RAD_count = 4
        NS_FLT_count = 2
        for i in range(Total_Curves):
            if i in NS:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_count)
                data[Curve_index[i]].Level    = '     101'
                NS_count += 1
            elif i in NS_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_RAD_count)
                data[Curve_index[i]].Level    = '     102'
                NS_RAD_count += 1
            elif i in RSF:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_count)
                data[Curve_index[i]].Level    = '     103'
                RSF_count += 1
            elif i in RSF_RAD:
                data[Curve_index[i]].ColorNum = '       ' + str(RSF_RAD_count)
                data[Curve_index[i]].Level    = '     104'
                RSF_RAD_count += 1
            elif i in NS_FLT:
                data[Curve_index[i]].ColorNum = '       ' + str(NS_FLT_count)
                data[Curve_index[i]].Level    = '     108'
                NS_FLT_count += 1
            else:
                data[Curve_index[i]].StatusNum = '01' + data[Curve_index[i]].StatusNum[2:]
                
    # Values of Hidden Status
    hid = '01'
    # Entity Type 100 - Circular Arc
    for i in range(len(ARC_index)):
        index = ARC_index[i]
        data[index].StatusNum = data[index].StatusNum[0:3] + '0' +data[index].StatusNum[4:]
    # Entity Type 102 - Composite Curve
    # Hide the composite curves
    for i in range(len(CCURVE_index)):
        index = CCURVE_index[i]
        statusNUM = data[index].StatusNum
        last = statusNUM[2:]
        statusNUM = hid+last
        data[index].StatusNum = statusNUM
    # Entity Type 110 - Line
    for i in range(len(LINE_index)):
        index = LINE_index[i]
        data[index].StatusNum = data[index].StatusNum[0:3] + '0' +data[index].StatusNum[4:]
    # Entity Type 126 - Rational B-Spline Curve
    for i in range(len(B_SPLINE_index)):
        index = B_SPLINE_index[i]
        data[index].StatusNum = data[index].StatusNum[0:3] + '0' +data[index].StatusNum[4:]
    # Rewrite file
    profile_name = fname[:-4]+'_'+pat
    file_new = profile_name + filetype
    os.chdir(new_dir)
    with open(file_new, 'w') as f:
        for i in range(len(Heading)):
            f.write(Heading[i])
            f.write('\n')
        for i in range(len(Data)):
            check = i%2
            if check == 0:
                index = int(i/2)
                f.write(data[index].EntityTypeL1)
                f.write(data[index].PDPointer)
                f.write(data[index].Structure)
                f.write(data[index].LineFontPattern)
                f.write(data[index].Level)
                f.write(data[index].View)
                f.write(data[index].TransMatrix)
                f.write(data[index].LabelDispAssoc)
                f.write(data[index].StatusNum)
                f.write(data[index].SectionSequenceNumL1)
                f.write('\n')
            else:
                index = int((i-1)/2)
                f.write(data[index].EntityTypeL2)
                f.write(data[index].LineWeight)
                f.write(data[index].ColorNum)
                f.write(data[index].ParameterLineCount)
                f.write(data[index].FormNum)
                f.write(data[index].Reserved)
                f.write(data[index].EntityLabel)
                f.write(data[index].EntitySubsriptNum)
                f.write(data[index].SectionSequenceNumL2)
                f.write('\n')
        for i in range(len(Parameters)):
            f.write(Parameters[i])
            f.write('\n')
