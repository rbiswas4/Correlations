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

def get_photTable(snsims, filter_query='SNID%50==0'):
    """
    Instance of `SNANASims`
    """
    snids = snsims.headData.reset_index().query(filter_query).SNID
    lcs = []
    for snid in snids:
        lcdata = snsims.get_SNANA_photometry(snid, keepSnid=True).lightCurve
        lcs.append(lcdata)
    # Need something if snid is None: 
    df = pd.concat(lcs)
    df['SNR'] = df.flux / df.fluxerr
    return df 

