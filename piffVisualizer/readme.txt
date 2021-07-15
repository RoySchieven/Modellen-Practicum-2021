Update July 2021:

This visualization section is largely copied from last years project. Two files are added: 

pyVis.py: This script takes care of 3D visualization. Make sure to have Mayavi installed before usage.

compactPIF no collagen.py: Does the same as compactPIF.py, but removes all collagen. It can be used to obtain a visualization without collagen blocking the view.



----------------------------------------------------

Original 2020:

I will briefly explain the files listed in this directory:

compactPIF.py: this compiles all of the pif files in the current folder (now 6) to a binary file format in alphabetical order. 
The output (the file named outputpiff) will then contain all of the frames and is now readable by pifVisualiser.

pifVisualizer: You can execute this by running ./pifVisualizer in Linux and it will grab the file outputpiff and display its contents in a sequential manner.

Makefile: These are the compilation instructions for pifVisualizer. To compile simply write: "make" while in this folder.

gridlogic and pifVisualizer are some sloppy cpp files to draw everything, never said it was going to be pretty ;).


