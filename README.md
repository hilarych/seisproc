# seisproc

Here are some colletion of useful functions for seismic data processing. The goal of this repository is to

1. Be able to do quick data analysis and visualization.
2. Have templates of frequenctly used routines for new projects.

The scripts are shared with the hope that they can be useful without any warranty. Scripts are subject to change. Please let me know if you notice any mistake. Thanks! 

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



