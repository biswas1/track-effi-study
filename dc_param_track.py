print("this script to make several param_file run hallc replay ")

import sys
import numpy as np
import os 
import re
import fileinput 
import shutil 

word = 'pxt_track_criterion'
print(word)
print ('Number of Arguments:', len(sys.argv), 'argements.')
print ('Argument List:', str(sys.argv))

#print(sys.argv[1])
a =float ( sys.argv[1])
b =float ( sys.argv[2])
step=float (sys.argv[3])
r=0

with open('PARAM/SHMS/GEN/ptracking.param','r') as f1:
    lines = f1.readlines()

print("ok upto this!")

for i in np.arange(a,b,step):
    i1=round(i,1) 
    newfilename = 'PARAM/SHMS/GEN/ptracking'+str(i)+'.param'
    with open(newfilename,'w') as f1:
        for line in lines:
            if word in line  :
                print(line)
                line1=re.split(r' = ',line)
                print(line1[1])
                line2=line.replace(line1[1],str(i1))
                print(line2)
                f1.write(line2)
                f1.write('\n')
            elif word not in line :
                f1.write(line)
            
    
    r=r+step
