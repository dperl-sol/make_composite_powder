#!/usr/bin/env python
import h5py
import numpy as np
import sys
import os

assert len(sys.argv) == 3, "Please supply two arguments: the input filename and the output filename, in that order."
assert (not os.path.isfile(sys.argv[2])), "Output file already exists."

if sys.argv[1].endswith('.lst'):
    print("Processing list of single files...")
    with open(sys.argv[1]) as f:
        files_list = f.read().splitlines()
    group = []
    for pattern in files_list:
        print (pattern)
        f = h5py.File(os.path.join(os.getcwd(),pattern),"r")
        group.append( np.array(f["maximum_value_composite"][:,:,]) )
        f.close()
    group_array = np.stack( group, axis=0 )
    final = np.amax(group_array, 0)
    out = h5py.File(sys.argv[2],"w")
    out["maximum_value_composite"] = final
    out.close()
        
elif sys.argv[1].endswith('master.h5'):
    print("Processing master HDF5 file...")
    f = h5py.File(sys.argv[1],"r")
    data_blocks = list(f["entry/data"].keys())
    group = []
    for block in data_blocks:
        group.append( np.amax(f["entry/data"][block][:,:,:], 0) )
    f.close()
    group_array = np.stack( group, axis=0 )
    final = np.amax(group_array, 0)
    out = h5py.File(sys.argv[2],"w")
    out["maximum_value_composite"] = final
    out.close()

