import os
import pandas as pd
from multiprocessing import Pool, cpu_count
import time
from lcfeats import process_fname
import argparse
import glob
import csv


def main(num_process, location, filter_query="SNID%50==0", outdir='./',
         format='hdf', serial=False):
    ts = time.time()
    files = glob.glob(location + "/*HEAD.FITS.gz")

    if serial:
        for rootfile in files:
            print(' Doing file ', rootfile)
            ht, pt = process_fname(rootfile, location, filter_query, outdir,
                                   True, format, 9) 
            if ht is None:
                print('Did not get anything from', rootfile)
    else:
        with Pool(num_process) as p:
            result = [p.apply(process_fname,
                              args=(rootfile, location, filter_query, outdir,
                                    True, format, 9))
                      for rootfile in files]
    te = time.time()
    return te - ts 

if __name__ == '__main__':
    simdir = '/users/rbiswas/data/lsst/opsimdata/rcc/kraken_2026/WFD'
    parser = argparse.ArgumentParser(description='write out compressed versions of sims maching classifications')
    parser.add_argument('--simdir', help='absolute path to directory eg. /users/rbiswas/data/lsst/opsimdata/rcc/kraken_2026/WFD',
                        default='./')
    args = parser.parse_args()
    simdir =  args.simdir

    with open('progress.csv', 'w+') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["location", "time_taken"])

    print('going to do files ... ')
    locs = list(reversed(os.listdir(simdir)))
    for loc in locs:
        print('locations:', loc)
    print('Now actually do it ... ', len(locs))
    for loc in locs:
        # construct query
        divisor = 50
        if int(loc[-2:]) in (51,61,62,63,64,84,90,91,93):
            divisor = 1
        query = 'SNID%{0}==0'.format(divisor)
        print('starting processing files in {0} at time {1}'.format(loc, time.time()))
        print(query)
        location = os.path.join(simdir, loc)
        num_process = cpu_count()
        time_taken = main(num_process, location, filter_query='SNID%50==0', outdir='./')
        with open('progress.csv', 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([loc, '{0}'.format(time_taken / 60.0)])
        
