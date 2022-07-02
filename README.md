# seisproc

Here, I share some simple and useful seismic processing routines. The goal of this project is to 

1. Be able to do quick data analysis and visualization.
2. Having templates of frequenctly used routines for new projects.

The scripts are shared with the hope that they can be useful without any warranty. Please let me know if you notice any mistake. Thanks! 

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



