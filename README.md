# How to run Metrics
- You should have python3 (hopefully works on 2, but not really checked).
- Install `future`, `fitsio` and `pandas` (hopefully the rest will just work
## 1. clone the LSST throughputs directory and export its location:
```
cd convenient_location
git clone https://github.com/lsst/throughputs.git
cd throughputs
export THROUGHPUTS_DIR=${PWD}
```
## 2. Install SNData
```
cd convenient_location
git clone https://github.com/LSSTDESC/SNData
cd SNDATA
# Change the branch to `https://github.com/LSSTDESC/SNData/tree/Issue/Add_snid`
python setup.py install --user
```
## 3. Run the compress script 
```python scripts/compress.py -h```
describes the options. What this will do is create a directory corresponding to each model and have a `summary_head` and
`summary_phot` hdf files. 

## 4.  
