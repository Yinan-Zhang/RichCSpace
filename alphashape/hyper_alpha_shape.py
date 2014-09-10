
"""
This class deal with the relation between every three balls in n-dimensional world
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'


import sys, os, math

sys.path.append('../basics/math')

from hyper_geometry import *
from Triangle import *

class Nerve:
	def __init__(self):
		pass;

	def nerve(self, spheres):
		'''Given a set of spheres, return triangles and edges based on their intersection relation'''
		edges = [];
		triangle_set = [];
		for sphere1 in spheres:
			for sphere2 in spheres:
				if not sphere1.intersects(sphere2) or sphere1 == sphere2:
					break;
				edges.append( (sphere1, sphere2) );
				for sphere3 in spheres:
					if sphere1.intersects(sphere3) and sphere2.intersects(sphere3):
						triangle = Triangle(sphere1, sphere2, sphere3);
						if triangle.is_filled():
							triangle_set.append(triangle);
					if sphere1.intersects(sphere3):
						edges.append( (sphere1, sphere3) );
					if sphere2.intersects(sphere3):
						edges.append( (sphere2, sphere3) );

		return edges, triangle_set;

	