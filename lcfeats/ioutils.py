"""
"""
from __future__ import division, absolute_import, print_function
__all__ = ['get_rootfile', 'get_photTable'] 

from sndata import SNANASims
import glob
import os
import pandas as pd

def get_rootfile(headname):
        return os.path.split(headname)[1].split('_HEAD')[0]

def get_photTable(snsims):
    """
    Instance of `SNANASims`
    """
    lcs = []
    for snid in snsims.headData.reset_index().SNID:
        lcdata = snsims.get_SNANA_photometry(snid, keepSnid=True).lightCurve
        lcs.append(lcdata)
        
    return pd.concat(lcs)

