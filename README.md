# seisproc

Here, I share some simple and useful seismic processing routines. The goal of this project is to 

1. Do quick data analysis and visualization.
2. Share light routines with minimum dependency that can be used as templates for many other projects.

The scripts are shared with the hope that they can be useful. They are distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version). Please let me know if you notice any mistake. Thanks! 

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



