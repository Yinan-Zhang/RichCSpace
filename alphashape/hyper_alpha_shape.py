
"""
This class deal with the relation between every three balls in n-dimensional world
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'


import sys, os, math
sys.path.append('../basics/math')

from numpy.linalg import matrix_rank

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
		for i in range(0, len(spheres)):
			sphere1 = spheres[i];
			for j in range(i, len(spheres)):
				sphere2 = spheres[j];
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

	def remove_same_edge(self, edges):
		'''two same edges could be (1,2) and (2,1), we need to remove one'''


	def betti_number( self, triangle_set, edge_set, edge_tri_dict ):
		'''Given some edges and triangles between edges, compute the first betti number.
		Needs to make sure there is no (1,2), (2,1) kind of situations in the edge_set'''
		added_triangles = [];
		vertices = [];
		for edge in edge_set:				# loop every edge
			if not edge[0] in vertices:		# put vertices in the vertices set
				vertices.append(edge[0]);
			if not edge[1] in vertices:
				vertices.append(edge[1]);	
			triangles = edge_tri_dict[edge];		# 
			for triangle in triangles:
				if triangle in triangle_set:
					continue;
				added_triangles.append(triangle);

		matrix = numpy.zeros((len(edge_set), len(added_triangles) ), dtype='int32');
		for i in range(0, len(edge_set)):
			for j in range(0, len(added_triangles)):
				if added_triangles[j] in edge_tri_dict[edge]:
					matrix[i, j] = 1;

		return len(edge_set) - len(vertices) + 1 - matrix_rank(matrix);


	def contract(self, spheres, triangle_set, graph_dict, edge_tri_dict):
		visited_vertices = [];
		while( True ):
			

		for sphere in spheres:
			neighbor_spheres = graph_dict[sphere]:
			if len(neighbor_spheres) == 0:
				continue;
			for neighbor in neighbor_spheres:
				edge = (sphere, neighbor);

		pass;

	