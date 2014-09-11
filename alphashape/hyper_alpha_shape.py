
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

	def __add2dict__(self, key, content, dictionary):
		if dictionary.has_key( key ):
			dictionary[key].append(content);
		else:
			dictionary[key] = [content];

	def nerve(self, spheres):
		'''Given a set of spheres
		@return edges: (sphere1, sphere2) pairs 
		@return triangle_set: triangle set
		@return graph_dict:	dictionary{ sphere1:[sphere2, sphere3,...] }
		@return edge_tri_dict: dictionary{ (sphere1, sphere2): triangle, .... }'''
		edges = [];
		triangle_set = [];
		graph_dict    = {};
		edge_tri_dict = {};
		for sphere1 in spheres:
			for sphere2 in spheres:
				if not sphere1.intersects(sphere2) or sphere1 == sphere2:
					break;
				if not (sphere1, sphere2) in edges:
					edges.append( (sphere1, sphere2) );
					self.__add2dict__(sphere1, sphere2, graph_dict);

				for sphere3 in spheres:
					if sphere1 == sphere3 or sphere2 == sphere3:
						continue;
					if sphere1.intersects(sphere3) and sphere2.intersects(sphere3):
						triangle = Triangle(sphere1, sphere2, sphere3);
						if triangle.is_filled():
							triangle_set.append(triangle);
							self.__add2dict__((sphere1,sphere2), triangle, edge_tri_dict);
							self.__add2dict__((sphere2,sphere1), triangle, edge_tri_dict);
							self.__add2dict__((sphere1,sphere3), triangle, edge_tri_dict);
							self.__add2dict__((sphere3,sphere1), triangle, edge_tri_dict);
							self.__add2dict__((sphere2,sphere3), triangle, edge_tri_dict);
							self.__add2dict__((sphere3,sphere2), triangle, edge_tri_dict);

		return edges, triangle_set, graph_dict, edge_tri_dict;

	