import sys, os, math

__all__ = [
  'Config'
]

'''
This file contains Config class that represents configurations for robots.
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

sys.path.append('../math')

from hyper_geometry import *

class Config( vec ):
	'Config class represents configurations of a robot'
	def __init__(self, pos):
		vec.__init__(self, pos);

	def dim(self):
		'''Returns the dimensions of the configuration'''
		return len(self);