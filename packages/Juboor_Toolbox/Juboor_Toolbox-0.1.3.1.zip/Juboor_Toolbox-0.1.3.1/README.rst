Juboor_Toolbox
--------

To use any of my tools, simply::

    >>> import Juboor_Toolbox as jt

Currently, The only tool (PCA) is in ML.py file.

To use::
	
	>>> Reduced_Data = jt.ML.PCA(data, # between 0-1)

	The data is an N x M array with only numeric values. 
		In order to reduce your data's dimensionality in either the Parameter
		or sample space, try transposing your data.