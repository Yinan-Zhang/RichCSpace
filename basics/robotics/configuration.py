import sys, os, math

__all__ = [
  'Config'
]

'''
This file contains Config class that represents configurations for robots.
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

class Config( list ):
	'Config class represents configurations of a robot'

	def dim(self):
		'''Returns the dimensions of the configuration'''
		return len(self);