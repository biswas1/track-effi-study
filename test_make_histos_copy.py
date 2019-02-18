from tkinter import*
import tkinter
import time, pickle
import ROOT as R 
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as mpl 
#mpl.rc('text',usetex=True)
mpl.rc('font', family='serif')

#Define the system clock 

startTime = time.time()

#open the dictionary produced via makeDataDict.py 
dd = pickle.load(open('dataDict_ystub_yp_on.pkl', 'rwb'))

# Chain ROOT files together per param setting
for tar, tar_dict in dd.items():
   
    # Initialize the tree chain lists
    dd[tar]['tree_chain'] = []
    tree_chain = []
    # Enumerate the individual param settings
    for index, mom_list in enumerate(dd[tar]['ystub_list']):
        # Initialze the TChain object for each momentum setting
        tree_chain = R.TChain('T')
        # Enumerate the list of ROOT files to be chained together
        for df_index, df_list in enumerate(dd[tar]['chain_list'][index]):
            tree_chain.Add(dd[tar]['chain_list'][index][df_index])
        # Populate the list of TChain objects for each momentum setting
        dd[tar]['tree_chain'].append(tree_chain)

# Save the dictionary with chained ROOT files into a pickle file
pickle.dump(dd, open('dataDictQNY.pkl', 'wb'), protocol=2)


electron_count_temp=[]
ystub_temp=[]
etr_effi_temp=[]
ystub=[]
tot_eff_temp=[]
electron_count=0

for tar, tar_dict in dd.items():
     # Add LaTeX format for target strings
     if (tar == 'c12') : tarStr = '{}^{12}C'
     for index, mom_list in enumerate(dd[tar]['ystub_list']):
         
         #ystub.append(dd[tar]['ystub_list'][index])
         tot_eff_temp.append(dd[tar]['tot_eff'][index]) 
         #nentries = dd[tar]['tree_chain'][index].GetEntries() 
         nentries = 100000
         # Loop over the entries in the trees
         print ('\nAnalyzing the %s target at %s GeV.  There are %d events to be analyzed.\n' % (tar.upper(), dd[tar]['ystub_list'][index], nentries))
         electron_count=0
         for entry in range(nentries):
             
             dd[tar]['tree_chain'][index].GetEntry(entry)
             if ((entry % 100000) == 0 and entry != 0) : print ('Analyzed %d events...' % entry)
             # Acquire the leaves of interest
             # PID variables
             lhgcNpeSum  = dd[tar]['tree_chain'][index].GetLeaf('P.hgcer.npeSum');   hgcNpeSum  = lhgcNpeSum.GetValue(0)
             lngcNpeSum  = dd[tar]['tree_chain'][index].GetLeaf('P.ngcer.npeSum');   ngcNpeSum  = lngcNpeSum.GetValue(0)                
             letracknorm = dd[tar]['tree_chain'][index].GetLeaf('P.cal.etracknorm'); etracknorm = letracknorm.GetValue(0)
             letotnorm   = dd[tar]['tree_chain'][index].GetLeaf('P.cal.etotnorm'); etotnorm = letotnorm.GetValue(0)
             # Target Variables
             ltheta  =  dd[tar]['tree_chain'][index].GetLeaf('P.gtr.th'); theta = ltheta.GetValue(0)
             lphi    =  dd[tar]['tree_chain'][index].GetLeaf('P.gtr.ph'); phi   = lphi.GetValue(0)
             lytar   =  dd[tar]['tree_chain'][index].GetLeaf('P.gtr.y'); ytar   = lytar.GetValue(0)
             # Phase space & acceptance variables
             ldelta  = dd[tar]['tree_chain'][index].GetLeaf('P.gtr.dp'); delta  = ldelta.GetValue(0)
             leprime = dd[tar]['tree_chain'][index].GetLeaf('P.gtr.p');  eprime = leprime.GetValue(0) # convert to mrad
             # Kinematic variables
             lw2     = dd[tar]['tree_chain'][index].GetLeaf('P.kin.W2'); w2 = lw2.GetValue(0)
             lq2     = dd[tar]['tree_chain'][index].GetLeaf('P.kin.Q2'); q2 = lq2.GetValue(0)
             lxbj    = dd[tar]['tree_chain'][index].GetLeaf('P.kin.x_bj'); xbj = lxbj.GetValue(0)
             #ltheta  = dd[tar]['tree_chain'][index].GetLeaf('P.kin.scat_ang_deg'); theta = ltheta.GetValue(0)
            
             
             # Define the fiducial cuts
             hgcNpeCut     = bool(hgcNpeSum < 2.0)
             ngcNpeCut     = bool(ngcNpeSum < 7.5)
             npeCut        = bool(hgcNpeCut or ngcNpeCut)
             deltaCut      = bool(delta < -10.0 or delta > 20.0)
             w2Cut         = bool(w2 < 2.0) # select the DIS regime
             etracknormCut = bool(etracknorm < 0.85)
             etotnormCut   = bool(etotnorm < 0.7)
             # Define the target cuts
             thetaCut = bool(theta < -1.0 or theta > 1.0) 
             phiCut   = bool(phi < -1.0 or phi > 1.0)
             ytarCut  = bool(ytar < -100.0 or ytar > 100.0)
             # Impose fiducial cuts
             if (hgcNpeCut or deltaCut or etotnormCut or thetaCut or phiCut or ytarCut or ytarCut or phiCut ) : continue
             electron_count += 1
             
 
         
         ystub_temp.append(dd[tar]['ystub_list'][index])
         electron_count_temp.append(electron_count)
             


print( "  *************\n   Check for crash1 \n  ************** \n")


ystub_array = np.asarray(ystub_temp,dtype=float)
tot_eff_array = np.asarray(tot_eff_temp,dtype=float)
electron_count_array = np.asarray(electron_count_temp,dtype=float)


print( "  *************\n   Check for crash2 \n  ************** \n")
index=[0]
ystub_array_cut = np.delete(ystub_array,index)
tot_eff_array_cut = np.delete(tot_eff_array,index)
electron_count_cut = np.delete(electron_count_array,index)

print(ystub_array_cut)
print(tot_eff_array_cut)
print(electron_count_cut)

effi_norm_yield = np.asarray(electron_count_cut / tot_eff_array_cut, dtype = float)
print(effi_norm_yield)

m1=max(ystub_array_cut)
print(m1)
m2=max(tot_eff_array_cut)
print(m2)
m3=max(effi_norm_yield)
print(m3)
print( "  *************\n   Check for crash3 \n  ************** \n")
X = np.asarray(ystub_array_cut , dtype = float)
Y1 = np.asarray(tot_eff_array_cut / m2 , dtype = float)
Y3 = np.asarray(effi_norm_yield / m3, dtype = float)

print(Y3)


#file1 = open("ystub_plot","a")
#file1.write(ystub)
#file1.close()
#for tar, tar_dict in dd.items():
#    dd[tar]['electron_count'] = []
#    dd[tar]['electron_count'].append(electron_count_array)

#pickle.dump(dd,open('dataDict_ystubplot.pkl','wb'),protocol=2)


#fig=mpl.figure()
mpl.figure()
#ax = fig.add_subplot(111)
#ax.text(0.25,0.09 ,r'X stub = 20 cm, Y stub = 20 cm, Xp = 1.0 rad',horizontalalignment='left', verticalalignment='bottom')
#ax.text(0.25,0.06,r'Run Number = 2548, Carbon, 21deg, 2.7GeV ',  horizontalalignment = 'left')
plt1 = mpl.scatter(X, Y1, color='g', marker = 'v', label = r'Fractional Tracking efficiency' )
#plt2 = mpl.scatter(X, Y2, color='r', marker = 'v')
plt3 = mpl.scatter(X, Y3, color='b', marker = 'v', label = r'Fractional ( Number of Electrons / Tracking Efficiency )')
mpl.title(r'Fractional ( Number of Electrons / Tracking Efficiency ) vs Xp Stub')
mpl.xlabel(r'Xp Stub Criteria (rad)')
mpl.ylabel(r'Fractional (Number of Electrons / Tracking efficiency)')
mpl.ylim(0.0,1.2)
mpl.xlim(0.0,1.0)
mpl.grid(linestyle='--')
mpl.text(2.0,0.3,r'X stub = 20 cm, Y stub =  7 cm, Yp = 0.2 rad')
mpl.text(2.0,0.2,r'Run Number = 2548, Carbon, 21deg, 2.7GeV')
mpl.text(1.9,0.1,r'PID Cuts: hgc > 2.0; -10% < delta < 22%; etotnorm > 0.7')
mpl.text(1.9,0.05,r'Target Quantity Cuts: -1< theta <1, -1< phi <1, -100< ytar <100 ')
mpl.legend( loc = 'upper right')
print( "  *************\n   Check for crash \n  ************** \n")
#mpl.plot(X,Y1)
mpl.show()

m4 = max(Y1)
print(m4)
Y4 = np.asarray( ((m4 - Y1)/m4)*100.0 , dtype = float)


mpl.figure()
plt1 = mpl.scatter(X, Y4, color='g', marker = 'v' )
mpl.title(r'%(Max Frac Track Effi - Frac Track Effi)/Max Frac Track Effi vs Xp Stub')
mpl.xlabel(r'Xp Stub Criteria (cm)')
mpl.ylabel(r'%(Max Frac Track Effi - Frac Track Effi)/Max Frac Track Effi')
mpl.ylim(0.0,2.0)
mpl.xlim(0.0,1.0)
mpl.grid(linestyle='--')
mpl.plot([0.0,30.0],[1.0,1.0],'b-',lw=1)
mpl.plot([0.0,30.0],[0.5,0.5],'b-',lw=1)
#mpl.text(2.0,0.3,r'Y stub = 7 cm, Yp stub = 0.2 rad, Xp = 0.4 rad')
#mpl.text(2.0,0.2,r'Run Number = 2548, Carbon, 21deg, 2.7GeV')
#mpl.text(1.9,0.1,r'PID Cuts: hgc > 2.0; -10% < delta < 22%; etotnorm > 0.7')
#mpl.text(1.9,0.05,r'Target Quantity Cuts: -1< theta <1, -1< phi <1, -100< ytar <100 ')
mpl.legend( loc = 'upper right')
print( "  *************\n   Check for crash \n  ************** \n")
#mpl.plot(X,Y1)
mpl.show()



"""
Y = np.delete(yel,index)
ystub_eff2 = np.delete(ystub_eff1,index)
#plt1= mpl.scatter(X,Y,color='b',marker='v')
plt1= mpl.scatter(ystub_eff1,ystub_eff1,color='b',marker='v')


#fig=plt.figure()
#plt.figure()
#
#plt.scatter(ystub_temp1,effi_nor_yield, color='g', marker = "v", ystub_temp1, yel_temp, color='r', marker = "v", ystub_temp1, etr_effi_temp, color='r', marker = "v" )
#plt.plot(ystub_temp1,effi_nor_yield,'r^', ystub_temp1, yel_temp, 'bs', ystub_temp1, etr_effi_temp, 'g^' )

#plt.grid()
#ax = fig.add_subplot(111) 
#ax.text(0.25,0.09 ,r'\textbf{X stub = 20 cm, Y stub = 20 cm, Xp = 1.0 rad}',horizontalalignment='left', verticalalignment='bottom')
#ax.text(0.25,0.06,r'\textbf{Run Number = 2548, Carbon, 21deg, 2.7GeV }',  horizontalalignment = 'left')
#plt.show()

"""
print("ok up to this !")
print ('\nThe analysis took %.3f minutes\n' % ((time.time() - startTime) / (60.)))
 

#ystub_temp.append(dd[tar]['ystub'])
