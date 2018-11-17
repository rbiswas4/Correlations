# How to
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
python setup.py install --user
```
### 3. 
