import sys, os, pygame, math
import numpy

from hyper_geometry import *

class triangle:
	def __init__( self, vert1, vert2, vert3 ):
		self.vertices = [vert1, vert2, vert3];

	def 