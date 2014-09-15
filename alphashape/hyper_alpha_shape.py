
"""
This class deal with the relation between every three balls in n-dimensional world
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'


import sys, os, math
sys.path.append('../basics/math')

from numpy.linalg import matrix_rank

from hyper_geometry import *
from l1_geometry 	import *
from Triangle 		import *

class Component:
	def __init__(self, comp_dict):
		self.dictionary = comp_dict;

	def contains(self, sphere):
		for triangle in self.dictionary.keys():
			if sphere in triangle.spheres:
				return True;
		return False;

	def spheres(self):
		'''get all spheres in the component'''
		spheres = {};
		for tri in self.dictionary.keys():
			for sphere in tri.spheres:
				if not spheres.has_key(sphere):
					spheres[sphere] = 1;

		return spheres.keys();


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
					continue;
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

		for tri1 in triangle_set:
			for tri2 in triangle_set:
				if tri1 == tri2:
					continue;
				if tri1.spheres[0] == tri2.spheres[0] or tri1.spheres[0] == tri2.spheres[1] or tri1.spheres[0] == tri2.spheres[2]:
					if tri1.spheres[1] == tri2.spheres[0] or tri1.spheres[1] == tri2.spheres[1] or tri1.spheres[1] == tri2.spheres[2]:
						if tri1.spheres[2] == tri2.spheres[0] or tri1.spheres[2] == tri2.spheres[1] or tri1.spheres[2] == tri2.spheres[2]:
							triangle_set.remove(tri2);

		return edges, triangle_set, graph_dict, edge_tri_dict;

	def build_topology_roadmap(self, components, graph_dict):
		'''Build the topology roadmap of C-space.
		@param components: contracted triangles (dictionaries).
		@param graph_dict: relation between each sphere'''

		def add2dict(dictionary, key, content):
			connections = self.connections_between(key, content, graph_dict);
			for i in range(0, connections):
				dictionary[key].append( content );

		#components = self.contract(triangle_set, edge_tri_dict);
		new_comps = [];
		for component in components:
			new_comps.append(Component(component));

		sphere_comp_dict = {}
		new_graph = {}
		for sphere in graph_dict.keys():
			containing_component = self.containing_component(sphere, new_comps);
			if containing_component is not None:
				sphere_comp_dict[sphere] = containing_component;

		for sphere in graph_dict.keys():
			if not sphere_comp_dict.has_key(sphere):   # This is a single sphere not in any component
				new_graph[sphere] = [];
				for neighbor in graph_dict[sphere]:	   # Loop every neighbor that connects with current sphere
					if not sphere_comp_dict.has_key(neighbor):
						#length = (v2(sphere.center[2], sphere.center[3])-v2(neighbor.center[2], neighbor.center[3])).r();
						#print sphere.center[2], sphere.center[3], neighbor.center[2], neighbor.center[3], length;
						add2dict(new_graph, sphere,	neighbor)
					elif not sphere_comp_dict[neighbor] in new_graph[sphere]:
						#new_graph[sphere].append(sphere_comp_dict[neighbor]);
						add2dict(new_graph, sphere,	sphere_comp_dict[neighbor]);
			elif( not new_graph.has_key(sphere_comp_dict[sphere]) ):# the sphere is in a component
				component = sphere_comp_dict[sphere]
				if not new_graph.has_key(component):
					new_graph[component] = [];
				neighbors = self.component_neighbors(component, graph_dict)
				for neighbor in neighbors:
					if not sphere_comp_dict.has_key(neighbor):
						#new_graph[sphere_comp_dict[sphere]].append(element);
						print "Comp <-> sphere"
						add2dict(new_graph, component, neighbor)
					elif not sphere_comp_dict[neighbor] in new_graph[component] and sphere_comp_dict[neighbor] != component:
						#new_graph[sphere_comp_dict[sphere]].append(sphere_comp_dict[element]);
						print "Comp <-> Comp"
						print component, sphere_comp_dict[neighbor]
						add2dict(new_graph, component, sphere_comp_dict[neighbor])
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
					added_triangles[triangle] = 1;

		matrix = numpy.zeros((len(edge_set), len(added_triangles.keys()) ), dtype='int32');
		for i in range(0, len(edge_set)):
			for j in range(0, len(added_triangles.keys())):
				if added_triangles.keys()[j] in edge_tri_dict[edge_set[i]]:
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
				component = self.contract_node(triangle, used, edge_tri_dict)
				dict_set.append(component)
		return dict_set;

	def contract_node(self, triangle, used, edge_tri_dict):
		'''Contract a triangle and its neighbor triangles'''
		neighbors = self.find_neighbor(triangle, edge_tri_dict)
		component = {};
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
		edge_set = self.component_edges(component);
		if self.betti_number(component, edge_set, edge_tri_dict) == 0:
			del component[triangle]
			return True;
		del component[triangle]
		return False;

	def component_edges(self, component):
		'''Get all edges of current component.'''
		edge_set = {}
		for triangle in component.keys():
			for edge in triangle.edges():
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

	def component_neighbors(self, component, graph_dict):
		'''get neighbors of a component'''
		neighbors = {};
		for sphere in component.spheres():
			for neighbor in graph_dict[sphere]:
				if not neighbors.has_key(neighbor):
					neighbors[neighbor] = 1;
		return neighbors.keys();

	def containing_component(self, sphere, components):
		'''Given a set of components, return the component that contains current sphere'''
		for component in components:
			if component.contains(sphere):
				return component;
		return None;

	def connections_between( self, elem1, elem2, graph_dict ):
		'''return the number of connections between the elem1 and the elem2'''

		if isinstance(elem1, hyper_sphere) and isinstance(elem2, hyper_sphere):
			return 1;
		elif isinstance(elem1, hyper_sphere) and isinstance(elem2, Component):
			conn = 0;
			for neighbor in graph_dict[elem1]:
				if elem2.contains(neighbor):
					conn += 1;
			return conn;
		elif isinstance(elem1, Component) and isinstance(elem2, hyper_sphere):
			conn = 0;
			for neighbor in graph_dict[elem2]:
				if elem1.contains(neighbor):
					conn += 1;
			return conn;
		elif isinstance(elem1, Component) and isinstance(elem2, Component):
			spheres = elem1.spheres();
			conn = 1;
			for sphere in spheres:
				for neighbor in graph_dict[sphere]:
					if elem2.contains(neighbor):
						conn += 1;
			return conn;