#!/apps/bin/python3

# Import various modules
import glob, string, pickle
import numpy as np

# Utilize glob to populate list of data & report files
df = glob.glob('ROOTfiles/ystub_root/yp_on/shms_replay_production_all_2548_100000_param_*.root')
rf = glob.glob('ystub_report/yp_on/replay_shms_all_production_2548_100000_*param*.report')
# Sort the lists for consistency
df.sort(); rf.sort()

# Define dictionaries
# Data dictionary
dd = { }
# Target dictionary
td = { 'c12' : 12.01 }
# Report file dictionary
rfd = { 'data'     : [],  # data file
        'rn'       : [],  # run number
        'pcent'    : [],  # central momentum
        'tamu'     : [],  # target amu
        'theta'    : [],  # spectrometer theta
        'ebeam'    : [],  # beam energy
        'q4a'      : [],  # bcm4a charge (mC, cut > 5 uA)
        'clt'      : [],  # computer live time
        'elt'      : [],  # electronic live time
        'etr_eff'  : [],  # electron tracking efficiency
        'scin_eff' : [],  # 3/4 trigger efficiency
        'psfactor' : [],  # el_real (ptrig2) pre-scale factor
        'xstub'    : [],  # xstub criteria
        'ystub'    : [],  # ystub criteria
        'xpstub'    : [], #xp stub criteria
        'ypstub'    : [] } # yptub criteria
  
# Store values of interest in lists
for index, run in enumerate(rf):
    rfd['data'].append(df[index])
    with open(rf[index]) as fobj:
        for line in fobj:
            data = line.split(':')
            # Kinematic configurations
            if ('Run Num'     in data[0]) : rfd['rn'].append(data[1].strip())
            if ('Momentum'    in data[0]) : rfd['pcent'].append(data[1].strip())
            if ('Target AMU'  in data[0]) : rfd['tamu'].append(data[1].strip())
            if ('Spec Theta'  in data[0]) : rfd['theta'].append(data[1].strip())
            if ('Beam Energy' in data[0]) : rfd['ebeam'].append(data[1].strip())
            # Charge and current
            if ('BCM4A Beam Cut Charge' in data[0]) : rfd['q4a'].append(''.join(list(filter(lambda x: x in string.digits + '.', data[1]))))
            # Live times (must be multiplied by 0.01 -> done later)
            if ('Pre-Scaled Ps2 SHMS Computer Live Time' in data[0])   : rfd['clt'].append(data[1][:8].strip())
            if ('OG 6 GeV Electronic Live Time (100, 150)' in data[0]) : rfd['elt'].append(data[1][:8].strip())
            # Tracking efficiencies
            if ('E SING FID TRACK EFFIC' in data[0]) : rfd['etr_eff'].append(data[1][:8].strip())
            # Trigger efficiency
            if ('3_of_4 EFF' in data[0]) : rfd['scin_eff'].append(data[1].strip())
            psdata = data[0].split('=')
            if ('Ps2_factor' in psdata[0]) : rfd['psfactor'].append(psdata[1].strip())
            stubdata = data[0].split('=')
            if ('xstub criteria' in stubdata[0]) : rfd['xstub'].append(stubdata[1][:6].strip())
            if ('ystub criteria' in stubdata[0]) : rfd['ystub'].append(stubdata[1][:6].strip())
            if ('xpstub criteria' in stubdata[0]) : rfd['xpstub'].append(stubdata[1][:6].strip())
            if ('ypstub criteria' in stubdata[0]) : rfd['ypstub'].append(stubdata[1][:6].strip())


# Enumerate targets and populate nested data dictionary sorted by target type
for tar_str, tar_amu in td.items():
    # Initialize dictionary
    dd[tar_str] = {}
    # Enumerate variables
    for var_str, var in rfd.items():
        # Initialize lists in data dictionary
        dd[tar_str][var_str] = []
        # Enumerate target list from report files
        for index, target in enumerate(rfd['tamu']):
            # Append lists when enumerated targets are identical
            if (float(td[tar_str]) == float(target)):
                dd[tar_str][var_str].append(rfd[var_str][index])


# Convert lists to arrays and store in data dictionary
for tar, tar_dict in dd.items():
    for rfd_var, rfd_list in dd[tar].items():
        if (rfd_var == 'data') : continue
        rfd_array = np.asarray(rfd_list, dtype = float)
        #del dd[tar][rfd_var] # really not sure why this is here, can probably delete
        if   (rfd_var == 'clt') : dd[tar][rfd_var] = rfd_array*0.01
        elif (rfd_var == 'elt') : dd[tar][rfd_var] = rfd_array*0.01
        else : dd[tar][rfd_var] = rfd_array
    # Calculate the per run efficiency
    dd[tar]['tot_eff'] = dd[tar]['etr_eff']*dd[tar]['scin_eff']*dd[tar]['clt']*dd[tar]['elt']
    # Calculate the efficiency (and pre-scale) corrected charge
    dd[tar]['eff_corr_q4a']    = dd[tar]['tot_eff']*dd[tar]['q4a']
    #dd[tar]['eff_ps_corr_q4a'] = dd[tar]['tot_eff']*dd[tar]['q4a'] / dd[tar]['psfactor']


# Parse root files into list corresponding the central momentum
for tar, tar_dict in dd.items():
    # Sorted array of unique central momentum settings
    #dd[tar]['ystub_list'] = np.unique(dd[tar]['ystub'])
    dd[tar]['ystub_list'] = np.asarray(dd[tar]['ystub'])
    # Initialize root file list containers
    rof_list     = []
    tmp_rof_list = []
    dd[tar]['chain_list'] = []
    # Initialize the efficiency corrected charge containers
    ecq_list     = []
    tmp_ecq_list = []
    dd[tar]['ecq_list'] = []
    # Enumerate condensed central momentum list
    for index, ystub_val in enumerate(dd[tar]['ystub_list']):
        # Make shallow copy of list so that when the temporary list is deleted an instance remains
        rof_list = list(tmp_rof_list)
        del tmp_rof_list[:]
        ecq_list = list(tmp_ecq_list)
        del tmp_ecq_list[:]
        # Cleanup vacancy as a result of deleting the instance of the temporary list
        if (len(rof_list) != 0) : 
            if (len(dd[tar]['chain_list'][index-1]) == 0) : dd[tar]['chain_list'].pop(index-1)
            dd[tar]['chain_list'].append(rof_list)
        # Enumerate the full central momentum list
        for iindex, pystub_val in enumerate(dd[tar]['ystub']):
            # If the central momenta from the two lists then fill root file containers
            if (dd[tar]['ystub_list'][index] == dd[tar]['ystub'][iindex]) :
                tmp_rof_list.append(dd[tar]['data'][iindex])
                #tmp_ecq_list.append(dd[tar]['eff_ps_corr_q4a'][iindex])
        # Populate the root file list corresponding to the respective momenta
        dd[tar]['chain_list'].append(tmp_rof_list)
        dd[tar]['ecq_list'].append(np.asarray(tmp_ecq_list))
    # Calculate the efficienct corrected charge for each target and momentum setting
    dd[tar]['ecq'] = []
    for index, ystub_val in enumerate(dd[tar]['ystub_list']):
        dd[tar]['ecq'].append(np.sum(dd[tar]['ecq_list'][index]))



# Save the dictionary into a pickle file
pickle.dump(dd, open('dataDict_ystub_yp_on.pkl', 'wb'), protocol =2 )
