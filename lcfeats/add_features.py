""" 
The methods of this module are maeant to apply to the summary / metadata file 
and the photometry file. 
"""
from __future__ import division, absolute_import, print_function

__all__ = ['Features']

import os
from . import example_data


class BaseFeatures(object):
    pass

class Features(BaseFeatures):
    """
    """
    def __init__(self, summary, photometry):
        
        self.summary = summary

        if 'SNR' not in photometry.columns.values:
            photometry.SNR = photometry.flux / photometry.fluxerr

        self.photometry = photometry

    @staticmethod
    def add_singleband_quants(photometry, summary, SNR_thresh=3.0):
        """
        Add quantities calculated from single band calculations

        Parameters
        ----------
        photometry : 

        summary : 

        SNR_thresh : float, defaults to 3.0 
            only observations with SNR greater than this threshold
            are considered
        """
        snr_thresh = 'SNR_greater_{:0.1f}_'.format(SNR_thresh)
        photometry = self.photometry.query('SNR > @SNR_thresh')
        df = photometry.groupby(['band', 'SNID']).agg(dict(mjd=[min, max, 'count'],
                                                           SNR=[max, np.median]))

        dfs_mjd = list(df.loc[b]['mjd'].rename(columns=dict(min=b+'_mjd_'+snr_thresh+'min',
                                                            max=b+'_mjd_'+snr_thresh+'max',
                                                            count=b+snr_thresh + 'numObs'))
                       for b in photometry.band.unique())

        dfs_snr = list(df.loc[b]['SNR'].rename(columns=dict(max=b+'_'+snr_thresh + 'max',
                                                            median=b+'_' + snr_thresh + 'median'))
                       for b in photometry.band.unique())

        for df in dfs_mjd:
            summary = summary.join(df)


        for df in dfs_snr:
            summary = summary.join(df)

        return summary
