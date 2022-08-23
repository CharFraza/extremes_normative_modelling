#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 10:10:47 2021

@author: chafra
"""

import os
import subprocess
import numpy as np

data_dir = '/project_cephfs/3022017.02/projects/big_data/data/ukb_processed_4'
idp_ids = []
with open(os.path.join(data_dir, 'idp_ids.txt'), 'r') as f:
    for line in f:
        idp_ids.append(line.strip())
idp_ids = idp_ids
#idp_ids = idp_ids[0:20]

# limit to a couple of interesting cases
#idp_ids= idp_ids[0]  
#idp_ids = ['25005-2.0']

# which type of model to run?
cov_type = 'bspline'  # 'int', 'bspline' or None
warp = 'WarpSinArcsinh' #WarpSinArcsinh'   # 'WarpBoxCox', 'Warp00
hyp0 = np.zeros(4)

cmd_qsub_base = ['/project_cephfs/3022017.02/projects/big_data/SubmitToCluster.py',
                 '-length', '102400',
                 '-memory', '10gb',
                 '-logfiledir /project_cephfs/3022017.02/projects/big_data/Torquefiles'
                ]

python_path = '/home/preclineu/chafra/.conda/envs/char/bin/python'
normative_path = '/home/preclineu/chafra/Desktop/PCNtoolkit/pcntoolkit/normative.py'

# set up dummy covariates
if cov_type is None:
    cov_file_dummy = os.path.join(data_dir, 'cov_male_dummy.txt')
else:
    cov_file_dummy = os.path.join(data_dir, 'cov_' + cov_type + '_male_dummy.txt')

for idp in idp_ids:
    print('Running IDP:', idp) 
    idp_dir = os.path.join(data_dir, idp)
   
    # set output dir 
    out_name = 'blr'
    if cov_type is not None:
        out_name += '_' + cov_type
    if warp is not None:
        out_name += '_' + warp
    os.makedirs(os.path.join(idp_dir,out_name), exist_ok=True)
    
    # configure the covariates to use
    if cov_type is None:
        cov_file_tr = os.path.join(idp_dir, 'cov_tr.txt')
        cov_file_te = os.path.join(idp_dir, 'cov_te.txt')
    else:
        cov_file_tr = os.path.join(idp_dir, 'cov_') + cov_type + '_tr.txt'
        cov_file_te = os.path.join(idp_dir, 'cov_') + cov_type + '_te.txt'
    resp_file_tr = os.path.join(idp_dir, 'resp_tr.txt')
    resp_file_te = os.path.join(idp_dir, 'resp_te.txt') 

    cd_cmd = ['cd', os.path.join(idp_dir,out_name), ';']
    fit_cmd = [python_path, 
               normative_path,
               '-c', cov_file_tr,
               '-t', cov_file_te,
               '-r', resp_file_te,
               '-a', 'blr',
               resp_file_tr,
               'optimizer=powell',
               'savemodel=True']
    if warp is not None:
        fit_cmd += ['warp=' + warp]
        fit_cmd += ['warp_reparam=True', 'optimizer=powell']
    fit_cmd += ';'
    
    prd_cmd = [python_path, 
               normative_path,
               '-f', 'predict',
               '-c', cov_file_dummy,
               'None']
    
    cmd_str = '"%s"' % str(' '.join(cd_cmd + fit_cmd + prd_cmd)) 
    cmd_qsub = cmd_qsub_base + ['-name', 'UKB_norm_' + idp,'-command', cmd_str]
    subprocess.Popen(' '.join(cmd_qsub), shell=True)
    print(cmd_str + '\n')
