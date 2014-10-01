
"""
This class deal with the relation between every three balls in n-dimensional world
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'


import sys, os, math, time
sys.path.append('../basics/math')

from numpy.linalg import matrix_rank
from hyper_geometry import *
from l1_geometry	import *
from Triangle	   import *

def GF2_matrix_rank( matrix, nrows, ncols ):
	'''Given a matrix, compute its rank'''
	rank = 0;
	n = min(nrows, ncols)
	for i in range(n):
		''' Find the pivot '''
		pivot_row = -1;
		for k in range(i, nrows):
			if matrix[k, i] == 1:
				pivot_row = k;
				break;

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

def betti_number(triangle_set, edge_list, edge_tri_dict):
	'''Given some edges and triangles between edges, compute the first betti number.
	Needs to make sure there is no (1,2), (2,1) kind of situations in the edge_list'''
	vertices = {};

	for edge in edge_list:			 # loop every edge
		if not vertices.has_key(edge[0]):# put vertices in the vertices set
			vertices[edge[0]] = 1;
		if not vertices.has_key(edge[1]):
			vertices[edge[0]] = 1;   
		
	#print "Creating a {0} matrix".format((len(edge_list), len(triangle_set)))
	matrix = numpy.zeros((len(edge_list), len(triangle_set) ), dtype='int32');
	triangle_list = triangle_set.keys()
	triangle_mapping = {}
	i = 0
	for triangle in triangle_list:
		triangle_mapping[triangle] = i;
		i += 1;
	i = 0
	for edge in edge_list:
		triangles = edge_tri_dict[edge]
		for triangle in triangles:
			if triangle_mapping.has_key(triangle):
				j = triangle_mapping[triangle]
				matrix[i, j] = 1;
		i += 1

	#print "Before Gaussian Elimination:"
	#print matrix, self.GF2_matrix_rank(matrix, len(edge_set), len(triangle_set))
	#print "After Gaussian Elimination:"
	#print matrix, matrix_rank(matrix)

	return len(edge_list) - len(vertices + 1 - self.GF2_matrix_rank(matrix, len(edge_list), len(triangle_set));

class Component:
	'''Define a 'component' as a set of spheres, such that there is no 1-d holes.
	meaning the first betti number is 0 '''
	def __init__(self, init_ball):
		'''A component should at least have one ball'''
		self.spheres = {}
		self.spheres[init_ball] = 1;
		self.edge_list = [];
		self.triangle_set = {};

	def spheres(self):
		return self.spheres.keys();

	def add_sphere(self, sphere, edge_tri_dict):
		'''determine if we can add a sphere to the component without increasing the 1-st betti number'''
		if self.spheres.has_key(sphere):
			return False;
			#raise Exception('You got a bug, the sphere is already in the component');
		
		new_triangles = {};
		new_edges = {};

		# Get new edges that might be added to the component
		for ball in self.spheres.keys(): 			# This step could be slow!!! (If the component has too many spheres already)
			if ball.intersects(sphere) and not new_edges.has_key((ball, sphere)) and not new_edges.has_key((sphere,ball)):
				new_edges[(ball, sphere)] = 1;

		# Get new triangles that might be added to the component
		for vert1, vert2 in new_edges.keys():
			edge_asct_tris = edge_tri_dict[(vert1, vert2)];	# triangles associated to an edge. 
															# might or might not be a triangle in self.triangle_set
			edge_asct_tris += edge_asct_tris[(vert2, vert1)];
			for tri in edge_asct_tris:
				if not new_triangles.has_key(tri):
					new_triangles[tri] = 1;

		# Now we have distinct new edges and new triangles while add a new sphere
		# Add them up.
		total_triangle_set = dict( self.triangle_set.items() + new_triangles.items() );
		total_edges 	   = self.edge_list + new_edges.keys();
		# Time to determine the betti number.
		betti_number 	   = betti_number(total_triangle_set, total_edges, edge_tri_dict);
		
		if betti_number == 0:				# If it will not increase the 1-st betti number
			self.spheres[sphere] = 1;		# add the sphere to the component
			self.triangle_set = total_edges;# update triangles in the component
			self.edge_list = total_edges;	# update edges in the component.
			return True;					# Tell caller the sphere can be added to the component
		return False;						# Tell caller the sphere cannot be added to the component

class Contraction:
	def __init__(self, spheres):
		self.spheres = spheres;
		self.graph = {};			# connections between spheres

		for sphere1 in self.spheres:
			for sphere2 in self.spheres:
				if sphere1 != sphere2 and sphere1.intersects(sphere2):
					if not self.graph.has_key(sphere1):
						self.graph[sphere1] = [sphere2];
					elif not sphere2 in self.graph[sphere1]:
						self.graph[sphere1].append(sphere2);

	def contract(self, triangle_set, edge_tri_dict, sphere_tri_dict):
		'''Contract a set of balls to several sets of balls, such that each set has first betti number of 0'''
		used_spheres = []
		component_set = [];

		for sphere in self.spheres:
			if not used_spheres.has_key[sphere]:
				component = self.contract_sphere(sphere, used_spheres, edge_tri_dict, sphere_tri_dict)
				if len(component.keys()) > 0:
					component_set.append(component)

		return component_set;

	def contract_sphere(self, sphere, used_spheres, edge_tri_dict, sphere_tri_dict):
		'''start from a sphere as the init of component, contract its neighbors as much as possible'''
		component = Component(sphere);
		neighbors = self.component_neighbor_spheres();
		find_new_sphere = True;

		while find_new_sphere:
			find_new_sphere = False;
			for neighbor in neighbors:
				if component.add_sphere(neighbor, edge_tri_dict):
					used_spheres[neighbor] = 1;
					find_new_sphere = True;

		return component;

	def component_neighbor_spheres(self, component, used_spheres, sphere_tri_dict):
		'''Find component's neighbor spheres'''
		comp_spheres = component.spheres();
		neighbors = {};
		for sphere in comp_spheres:
			curr_neighbors = self.graph[sphere];
			for curr_neighbor in curr_neighbors:
				if not used_spheres.has_key[curr_neighbor] and not neighbors.has_key(curr_neighbor):
					neighbors[curr_neighbor] = 1;
		return curr_neighbors.keys();



