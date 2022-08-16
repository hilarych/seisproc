# seisproc

Here are some collections of useful functions for seismic data processing. The goal of this repository is to

1. Be able to do quick data analysis and visualization.
2. Have templates of frequenctly used routines for new projects.

The codes in this repository are still in experiment and proliminary stage. Scripts are subject to change. 

@ Hilary Chang ([hilarych@mit.edu](mailto:hilarych@mit.edu))

## Usage:

Download the repo in terminal at `your_packages_dir`:
```console
git clone https://github.com/hilarych/seisproc.git
```

In the Python script:
```python
import sys
sys.path.append('your_packages_dir/')
import seisproc as sep

# eg. Using the fk functions
sep.fk_filter(...) 
```



