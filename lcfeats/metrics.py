""" 
The methods of this module are maeant to apply to the summary / metadata file 
and the photometry file. 
"""
from __future__ import division, absolute_import, print_function

__all__ = ['Metrics']

import os
from . import example_data
import pandas as pd
import numpy as np


class Metrics(object):
    """
    """
    def __init__(self, summary, photometry, metrics_fname):
        self.summary = summary 
        self.photometry = photometry
        self.metrics_fname = metrics_fname

    def metric_list(self):
        """
        """
        metric_list = list()
        # calculate 
        metric_list.append('exposure_time_sb_snr')
        metric_list.append(('num_mjd_range', self._add_num_mjd_range))
        return metric_list


    def add_num_mjd_range(self, SNR_thresh=1.0):
        filt = 'SNR_greater_{0:0.1f}'.format(SNR_thresh)
        ss = self.summary
        ss = self.num_mjd_range(ss, myfilt=filt,
                                quants=['mjd_max', 'mjd_min'])
        self.summary = ss

    @staticmethod
    def num_mjd_range(ss, myfilt='SNR_greater_3.0',
                      quants=['mjd_max', 'mjd_min']):
        """
        """
    
        mydict = dict()
        required_quants = list('lsst'+ b + '_' + myfilt + '_' + quants[0] for b in list('ugrizy'))\
                        + list('lsst'+ b + '_' + myfilt + '_' + quants[1] for b in list('ugrizy'))

	# Should include code to recalculate required quantities
        for required_quant in required_quants:
            if required_quant not in ss.columns.values:
                # add required quants to ss
                print(" Don't have quantity {}".format(required_quant))
                raise NotImplementedError('Not yet implemented way to add these')

        # return required_quants
        for b in list('ugrizy'):
            mykey = 'lsst' + b + '_' + myfilt + '_mjd_range'
            mycalc = ss['lsst' + b + '_' + myfilt + '_mjd_max'] - \
                     ss['lsst' + b + '_' + myfilt + '_mjd_min']
            mydict[mykey] = mycalc
    
        return ss.join(pd.DataFrame(mydict))


