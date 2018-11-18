"""
"""
from __future__ import division, absolute_import, print_function
__all__ = ['get_rootfile', 'get_photTable', 'process_fname'] 

from sndata import SNANASims
import glob
import os
import pandas as pd

def process_fname(fname, location, filter_query="SNID%50==0", outDir='./',
                  write=False, format='hdf', complevel=9):
    """
    fname : string, mandatory
	the name of a head file.
    location : string, mandatory
	directory in which the files are
    filter_query: string, defaults to "SNID%50 == 0"
	query to be run selecting the objects from both the head and phot file.
    outDir : string, defaults to './'
       directory where stuff will be written if write is True	
    write : Bool, defaults to False
    format : string, defaults to hdf
	{'hdf'|'csv'}
    complevel : int, defaults to 9
	Actually not used, but enforced
    
    """
    # print(rootfile)
    # return
    rootfile = get_rootfile(fname)
    snsims = SNANASims.fromSNANAfileroot(rootfile, coerce_inds2int=True, location=location, gzipped=True)

    # If the SNANA Sims represented is None, we are done
    if snsims is None:
        return None, None
    ht = snsims.headData.reset_index().query('SNID%50==0')
    if len(ht) == 0:
        return None, None

    phottable = get_photTable(snsims, filter_query=filter_query)
    dirname = os.path.split(location)[-1] + '_compressed'
    # Use the one below instead of the one above, not tested
    # dirname = os.path.basename(location) + '_compressed'
    dirloc = os.path.join(outDir, dirname)
    if not os.path.exists(dirloc):
        os.mkdir(dirloc)
    
    if write:
        key = rootfile.split('-')[-1]
        if format == 'hdf':
            phottable.to_hdf(os.path.join(dirloc, 'summary' + '_phot.hdf'), key=key, complib='zlib', complevel=9)
            ht.to_hdf(os.path.join(dirloc, 'summary' + '_head.hdf'), key=key,complib='zlib', complevel=9)
        elif format == 'csv':
            phottable.to_csv(os.path.join(dirloc, rootfile + '_phot.csv.gz'), compression='gzip')
            ht.to_csv(os.path.join(dirloc, rootfile + '_head.csv.gz'), compression='gzip')
        else:
            raise NotImlementedError('formmat not implemented') 

    return ht, phottable

def get_rootfile(headname):
        return os.path.split(headname)[1].split('_HEAD')[0]

def get_photTable(snsims, filter_query='SNID%50==0'):
    """
    Instance of `SNANASims`
    """
    if snsims is None:
        return None
    snids = snsims.headData.reset_index().query(filter_query).SNID
    lcs = []
    for snid in snids:
        lcdata = snsims.get_SNANA_photometry(snid, keepSnid=True).lightCurve
        if len(lcdata) > 9:
            lcs.append(lcdata)
    # Need something if snid is None: 
    if len(lcs) == 0:
        return lcs
    df = pd.concat(lcs)
    df['SNR'] = df.flux / df.fluxerr
    return df 

