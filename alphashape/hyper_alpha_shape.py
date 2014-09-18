
"""
This class deal with the relation between every three balls in n-dimensional world
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'


import sys, os, math
sys.path.append('../basics/math')

from numpy.linalg import matrix_rank

from hyper_geometry import *
from l1_geometry	import *
from Triangle	   import *

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
		@return graph_dict: dictionary{ sphere1:[sphere2, sphere3,...] }
		@return edge_tri_dict: dictionary{ (sphere1, sphere2): triangle, .... }
		@return sphere_tri_dict: dictionary{ sphere1: [triangle1, tri2...], ... }'''
		edges		   = [];
		triangle_set	= [];
		graph_dict	  = {};
		edge_tri_dict   = {};
		sphere_tri_dict = {}
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

		no_same_tri_set = [];
		same = [];
		for tri1 in triangle_set:
			if tri1 in same:
				continue;
			no_same_tri_set.append(tri1);
			for tri2 in triangle_set:
				if tri1 == tri2:
					continue;
				if tri1.spheres[0] == tri2.spheres[0] or tri1.spheres[0] == tri2.spheres[1] or tri1.spheres[0] == tri2.spheres[2]:
					if tri1.spheres[1] == tri2.spheres[0] or tri1.spheres[1] == tri2.spheres[1] or tri1.spheres[1] == tri2.spheres[2]:
						if tri1.spheres[2] == tri2.spheres[0] or tri1.spheres[2] == tri2.spheres[1] or tri1.spheres[2] == tri2.spheres[2]:
							#triangle_set.remove(tri2);
							same.append(tri2);

		print "initially we have {0} triangles".format(len(triangle_set))

		for tri in no_same_tri_set:
			self.__add2dict__(tri.spheres[0], tri, sphere_tri_dict);
			self.__add2dict__(tri.spheres[1], tri, sphere_tri_dict);
			self.__add2dict__(tri.spheres[2], tri, sphere_tri_dict);

		return edges, no_same_tri_set, graph_dict, edge_tri_dict, sphere_tri_dict;

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
				for neighbor in graph_dict[sphere]:	# Loop every neighbor that connects with current sphere
					if not sphere_comp_dict.has_key(neighbor):
						add2dict(new_graph, sphere, neighbor)
					elif not sphere_comp_dict[neighbor] in new_graph[sphere]:
						add2dict(new_graph, sphere, sphere_comp_dict[neighbor]);
			elif( not new_graph.has_key(sphere_comp_dict[sphere]) ):# the sphere is in a component
				component = sphere_comp_dict[sphere]
				if not new_graph.has_key(component):
					new_graph[component] = [];
				neighbors = self.component_neighbors(component, graph_dict)
				for neighbor in neighbors:
					if not sphere_comp_dict.has_key(neighbor):
						add2dict(new_graph, component, neighbor)
					elif not sphere_comp_dict[neighbor] in new_graph[component] and sphere_comp_dict[neighbor] != component:
						add2dict(new_graph, component, sphere_comp_dict[neighbor])
		return new_graph;

	def GF2_matrix_rank( self, matrix, nrows, ncols ):
		rank = 0;
		n = min(nrows, ncols)
		for i in range(n):
			''' Find the pivot '''
			pivot_row = -1;
			for k in range(i, nrows):
				if matrix[k, i] == 1:
					pivot_row = k;
					break;

			#print matrix;
			#print pivot_row;
			''' If there is no pivot, then go to the next row '''
			if pivot_row == -1:
				continue;
			for j in range(ncols):
				temp = matrix[i, j]
				matrix[i,j] = matrix[pivot_row, j]
				matrix[pivot_row, j] = temp
			pivot_row = i
			rank += 1;
			for k in range(nrows):
				if k == pivot_row or matrix[k, i] == 0:
					continue;
				for j in range(ncols):
					matrix[k, j] = matrix[k, j] ^ matrix[pivot_row, j]
		return rank;

	def betti_number( self, triangle_set, edge_set, edge_tri_dict ):
		'''Given some edges and triangles between edges, compute the first betti number.
		Needs to make sure there is no (1,2), (2,1) kind of situations in the edge_set'''
		vertices = [];

		for edge in edge_set:			   # loop every edge
			if not edge[0] in vertices:	 # put vertices in the vertices set
				vertices.append(edge[0]);
			if not edge[1] in vertices:
				vertices.append(edge[1]);   
			
		print "Creating a {0} matrix".format((len(edge_set), len(triangle_set)))
		matrix = numpy.zeros((len(edge_set), len(triangle_set) ), dtype='int32');
		for i in range(0, len(edge_set)):
			for j in range(0, len(triangle_set)):
				if triangle_set.keys()[j] in edge_tri_dict[edge_set[i]]:
					matrix[i, j] = 1;

		#print "Before Gaussian Elimination:"
		#print matrix, self.GF2_matrix_rank(matrix, len(edge_set), len(triangle_set))
		#print "After Gaussian Elimination:"
		#print matrix, matrix_rank(matrix)

		return len(edge_set) - len(vertices) + 1 - self.GF2_matrix_rank(matrix, len(edge_set), len(triangle_set));

	def contract(self, triangle_set, edge_tri_dict, sphere_tri_dict):
		'''Contract a set of triangles to several sets of triangles, such that each set has first betti number of 0'''
		visited_vertices = [];
		dict_set = [];  # we use a dictionary to store a set of triangles;
						# The set of dictionaries is the set of contracted triangles.
		used = {};

		i = 0;
		for triangle in triangle_set:
			print "trying triangle: {0}".format(i);
			i+=1
			if not used.has_key(triangle):
				component = {};
				# Do it recursively
				self.contrct_triangle_recursive(component, triangle, used, edge_tri_dict, sphere_tri_dict)
				#component = self.contract_triangle(triangle, used, edge_tri_dict, sphere_tri_dict)
				if len(component.keys()) > 0:
					dict_set.append(component)
		return dict_set;

	def contrct_triangle_recursive( self, component, triangle, used, edge_tri_dict, sphere_tri_dict ):
		'''Contract a triangle and its neighbor triangles'''
		if used.has_key(triangle) or not self.is_useful(component, triangle, edge_tri_dict):
			return;

		component[triangle] = 1
		used[triangle] = True

		neighbors = self.find_component_neighbors(component, edge_tri_dict, sphere_tri_dict)
		print len(neighbors)
		for neighbor in neighbors:
			self.contrct_triangle_recursive(component, neighbor, used, edge_tri_dict, sphere_tri_dict);

	def contract_triangle(self, triangle, used, edge_tri_dict, sphere_tri_dict):
		'''Contract a triangle and its neighbor triangles'''
		neighbors = self.find_neighbor(triangle, edge_tri_dict, sphere_tri_dict)
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
					new_neighbors = self.find_neighbor(neighbor, edge_tri_dict, sphere_tri_dict)
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

	def find_component_neighbors( self, component, edge_tri_dict, sphere_tri_dict ):
		'''find the neighbor triangle of a given component'''
		neighbors = {};
		for tri in component.keys():
			tri_neighbors = self.find_neighbor(tri, edge_tri_dict, sphere_tri_dict);
			for neighbor in tri_neighbors:
				if not neighbors.has_key(neighbor):
					neighbors[neighbor] = 1;
		return neighbors;

	def find_neighbor(self, triangle, edge_tri_dict, sphere_tri_dict):
		'''Find neighbor triangles of a given triangle'''
		neighbors = {};
		for sphere in triangle.spheres:
			neighbor_tris = sphere_tri_dict[sphere];
			for tri in neighbor_tris:
				if tri != triangle and not neighbors.has_key(tri):
					neighbors[tri] = 1;
		'''
		edges = triangle.edges();
		for edge in edges:
			if edge_tri_dict.has_key(edge):
				for tri in edge_tri_dict[edge]:
					if not neighbors.has_key(tri):
						neighbors[tri] = 1;
		'''
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

		if (isinstance(elem1, hyper_sphere) or isinstance(elem1, l1_sphere)) and (isinstance(elem2, hyper_sphere) or isinstance(elem2, l1_sphere)):
			return 1;
		elif (isinstance(elem1, hyper_sphere) or isinstance(elem1, l1_sphere)) and isinstance(elem2, Component):
			conn = 0;
			for neighbor in graph_dict[elem1]:
				if elem2.contains(neighbor):
					conn += 1;
			return conn;
		elif isinstance(elem1, Component) and (isinstance(elem2, hyper_sphere) or isinstance(elem2, l1_sphere)):
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
