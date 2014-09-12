
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
			for j in range(0, len(spheres)):
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

	def build_topology_roadmap(self, sphere_set, triangle_set, edge_tri_dict, graph_dict):
		'''Build the topology roadmap of C-space'''

		def add2dict(dictionary, key, content):
			if not dictionary.has_key(key):
				dictionary[key] = [];
			connections = self.connections_with( key, content, graph_dict );
			for i in range(0, connections):
				dictionary[key].append( content );

		components = self.contract(triangle_set, edge_tri_dict);
		sphere_comp_dict = {}
		new_graph = {}
		for sphere in graph_dict.keys():
			containing_component = self.containing_component(sphere, components):
			if containing_component is not None:
				sphere_comp_dict[sphere] = containing_component;

		for sphere in graph_dict.keys():
			if not sphere_comp_dict.has_key(sphere):   # This is a single sphere not in any component
				new_graph[sphere] = [];
				for element in graph_dict[sphere]:	   # Loop every element that connects with current sphere
					if not sphere_comp_dict.has_key(element):
						add2dict(new_graph, sphere,	element)
					elif not sphere_comp_dict[element] in new_graph[sphere]:
						#new_graph[sphere].append(sphere_comp_dict[element]);
						add2dict(new_graph, sphere,	sphere_comp_dict[element]);
			else:										# the sphere is in a component
				if not new_graph.has_key(sphere_comp_dict[sphere]):
					new_graph[sphere_comp_dict[sphere]] = [];
				for element in graph_dict[sphere]:
					if not sphere_comp_dict.has_key(element)：
						#new_graph[sphere_comp_dict[sphere]].append(element);
						add2dict(new_graph, sphere_comp_dict[sphere], element)
					elif not sphere_comp_dict[element] in new_graph[sphere_comp_dict[sphere]]:
						#new_graph[sphere_comp_dict[sphere]].append(sphere_comp_dict[element]);
						add2dict(new_graph, sphere_comp_dict[sphere], sphere_comp_dict[element])
		return new_graph;


	def betti_number( self, triangle_set, edge_set, edge_tri_dict ):
		'''Given some edges and triangles between edges, compute the first betti number.
		Needs to make sure there is no (1,2), (2,1) kind of situations in the edge_set'''
		added_triangles = {};
		vertices = [];
		for edge in edge_set:				# loop every edge
			if not edge[0] in vertices:		# put vertices in the vertices set
				vertices.append(edge[0]);
			if not edge[1] in vertices:
				vertices.append(edge[1]);	
			triangles = edge_tri_dict[edge];		# 
			for triangle in triangles:
				if triangle not in added_triangles:
					added_triangles[triangle];

		matrix = numpy.zeros((len(edge_set), len(added_triangles.keys()) ), dtype='int32');
		for i in range(0, len(edge_set)):
			for j in range(0, len(added_triangles.keys()):
				if added_triangles[j] in edge_tri_dict[edge]:
					matrix[i, j] = 1;

		return len(edge_set) - len(vertices) + 1 - matrix_rank(matrix);

	def contract(self, triangle_set, edge_tri_dict):
		'''Contract a set of triangles to several sets of triangles, such that each set has first betti number of 0'''
		visited_vertices = [];
		dict_set = []; 	# we use a dictionary to store a set of triangles;
						# The set of dictionaries is the set of contracted triangles.
	    used = {};
		for triangle in triangle_set:
			if not used.has_key(triangle):
				component = self.contract(triangle, used, edge_tri_dict)
				dict_set.append(component)
		return dict_set;

	def contract(self, triangle, used, edge_tri_dict):
		'''Contract a triangle and its neighbor triangles'''
		neighbors = self.find_neighbor(triangle, edge_tri_dict)
		component[triangle] = 1
		used[triangle] = True
		found = True;
		while found:
			found = False;
			for neighbor in neighbors.keys():
				if not used.has_key(neighbor) and self.is_useful(component, neighbor, edge_tri_dict):
					component[neighbor] = 1
					used[neighbor] = True
					del neighbors[neighbor]
					found = True;
					new_neighbors = self.find_neighbor(neighbor, edge_tri_dict)
					for new_triangle in new_neighbors.keys():
						if not used.has_key(new_triangle) and not neighbors.has_key(new_triangle):
							neighbors[new_triangle] = 1
		return component;

	def is_useful(self, component, triangle, edge_tri_dict):
		'''determine if a triangle can be added to current component without increasing 1st betti number.'''
		component[triangle] = 1
		edge_set = component_edges(component);
		if self.betti_number(component, edge_set, edge_tri_dict) == 0:
			del component[triangle]
			return True;
		del component[triangle]
		return False;

	def component_spheres(self, component):
		'''Get all spheres in a component'''
		spheres = [];
		for triangle in component.keys():
			for sphere in triangle.spheres:
				if not sphere in spheres:
					spheres.append(sphere):
		return spheres;


	def component_edges(self, component):
		'''Get all edges of current component.'''
		edge_set = {}
		for triangle in component.keys():
			for edge in triangle.edges:
				(a, b) = edge
				if not edge_set.has_key((a, b)) and not edge_set.has_key((b, a)):
					edge_set[(a, b)] = 1
		return edge_set.keys();

	def find_neighbor(self, triangle, edge_tri_dict):
		'''Find neighbor triangles of a given triangle'''
		neighbors = {};
		edges = triangle.edges();
		for edge in edges:
			if edge_tri_dict.has_key(edge):
				for tri in edge_tri_dict[edge]:
					if not neighbors.has_key(tri):
						neighbors[tri] = 1;
		return neighbors

	def component_contains( self, component, sphere ):
		'''determine if a component contains a sphere'''
		for triangle in component.keys():
			if sphere in triangle.spheres:
				return True;
		return False;

	def containing_component(self, sphere, components):
		'''Given a set of components, return the component that contains current sphere'''
		for component in components:
			if self.component_contains(component, sphere):
				return component;
		return None;

	def connections_between( self, elem, component, graph_dict ):
		'''return the number of connections between the element and the component'''
		if isinstance(elem, sphere):	# a single sphere
			result = 0;
			neighbors = graph_dict[elem];
			for neighbor in neighbors:
				if self.component_contains(component, neighbor):
					result += 1;
			return result;
			pass;
		elif isinstance(elem, dict):	# a set of triangles
			spheres = self.component_spheres(elem);
			result = 0;
			for sphere in spheres:
				neighbors = graph_dict[elem];
				for neighbor in neighbors:
					if self.component_contains(component, sphere):
						result += 1;
			return result;


	