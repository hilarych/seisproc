# seisproc

This is a long-term project for sharing simple and useful seismic processing routines. The goal of this project is to share light routines with minimum dependency that can be easily integrated into many other projects.

## Usage:

Download the repo in terminal:
'''
package_dir$ git clone https://github.com/hilarych/seisproc.git
'''

In the Python script:
'''
import sys
sys.path.append('package_dir/')
import seisproc as se

# Using the fk functions
se.fk 
'''



## Contents:

- **util.py**: Basic signal processing treatments
- **fk.py**: fk domain processing
- **plot.py**: Functions for visualization
- **ax.py**: Objects and functions for plotting


The scripts are distributed under the terms of the GNU General Public License as 
published by the Free Software Foundation (version 3 or later version).

@ Hilary Chang ([hilarych@mit.edu](hilarych@mit.edu))

