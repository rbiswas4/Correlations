""" 
Features are quantities that are already recorded in the simulation summary
files, or are calculated from the photometry. The philosophy behind these
quantities is that several `metrics` are calculable from such quantities, and
therefore, the first step is to calculate the set of Features required by a
list of metrics. Metrics are then calculated in a second step. This should
enable quick re-calculation of some metrics.
"""
from __future__ import division, absolute_import, print_function
__all__ = ['Features']

import os
import numpy as np
from . import example_data


def diffmedian(series):
    series = series.sort_values().diff()
    return np.nanmedian(series)
def diffstd(series):
    series = series.sort_values().diff()
    return np.std(series)


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
    def diffmedian(series):
        series = series.sort_values().diff()
        return np.nanmedian(series)
    
    @staticmethod
    def diffstd(series):
        series = series.sort_values().diff()
        return np.std(series)

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
        snr_thresh = '_SNR_greater_{:0.1f}'.format(SNR_thresh)
        photometry = photometry.query('SNR > @SNR_thresh')
        df = photometry.groupby(['band', 'SNID']).agg(dict(mjd=[min, max, 'count',
                                                                diffmedian, diffstd],
                                                           SNR=[max, np.nanmedian],
                                                           SIM_MAGOBS=[np.nanmedian]))

        dfs_mjd = list(df.loc[b]['mjd'].rename(columns=dict(min=b+snr_thresh+'_mjd'+'_min',
                                                            max=b+snr_thresh+'_mjd'+'_max',
                                                            count=b+snr_thresh + '_numObs',
                                                            diffmedian=b+snr_thresh + '_diffmedian',
                                                            diffstd=b+snr_thresh + '_diffstd'))
                       for b in photometry.band.unique())

        dfs_snr = list(df.loc[b]['SNR'].rename(columns=dict(max=b+snr_thresh+'_SNR'+'_max',
                                                            nanmedian=b+snr_thresh+'_SNR'+'_median'))
                       for b in photometry.band.unique())

        dfs_magobs = list(df.loc[b]['SIM_MAGOBS'].rename(columns=dict(nanmedian=b+snr_thresh+'_SIM_MAGOBS'+'_median'))
                          for b in photometry.band.unique())

        for df in dfs_mjd:
            print(df.columns)
            print(summary.columns)
            summary = summary.join(df)


        for df in dfs_snr:
            summary = summary.join(df)

        for df in dfs_magobs:
            summary = summary.join(df)

        return summary
