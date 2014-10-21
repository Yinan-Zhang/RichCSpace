"""
This class deal with the relation between every three balls in n-dimensional world
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'

import pdb

import sys, os, math, time, pygame, copy
sys.path.append('../basics/math')

from numpy.linalg import matrix_rank
from hyper_geometry import *
from l1_geometry	import *
from Triangle	   import *

def merge_sets( dict1, dict2 ):
	result = {};
	for key in dict1.keys():
		if not result.has_key(key):
			result[key] = 1
	for key in dict2.keys():
		if not result.has_key(key):
			result[key] = 1;
	return result;

def draw_triangle2( triangle, surface, color ):
	points = [ (int(triangle.spheres[0].center[0]), int(triangle.spheres[0].center[1]) ), (int(triangle.spheres[1].center[0]), int(triangle.spheres[1].center[1]) ), ( int(triangle.spheres[2].center[0]), int(triangle.spheres[2].center[1] )) ];
	pygame.draw.polygon(surface, color, points, 5);
	return;

def draw_triangle( triangle, surface, color ):
	points = [ (int(triangle.spheres[0].center[0]), int(triangle.spheres[0].center[1]) ), (int(triangle.spheres[1].center[0]), int(triangle.spheres[1].center[1]) ), ( int(triangle.spheres[2].center[0]), int(triangle.spheres[2].center[1] )) ];
	pygame.draw.polygon(surface, color, points, 1);
	return;

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
			vertices[edge[1]] = 1;
		
	#print "Creating a {0} matrix".format((len(edge_list), len(triangle_set)))
	matrix = numpy.zeros((len(edge_list), len(triangle_set) ), dtype='int32');
	triangle_list = triangle_set.keys()
	triangle_mapping = {}
	i = 0
	for triangle in triangle_list:
		triangle_mapping[triangle] = i;
		i += 1;
	i = 0
	for v1, v2 in edge_list:
		if edge_tri_dict.has_key((v1,v2)):
			edge = (v1,v2)
		else:
			edge = (v2,v1)

		if not edge_tri_dict.has_key(edge):
			continue;

		triangles = edge_tri_dict[edge]
		for triangle in triangles:
			if triangle_set.has_key(triangle) and triangle_mapping.has_key(triangle):
				j = triangle_mapping[triangle]
				matrix[i, j] = 1;
		i += 1

	#print "---- Betti Number ----"
	#print "matrix:\n{0}".format(matrix);

	#print "Triangles: {0}".format(len(triangle_list));
	#print "edges: {0}".format(len(edge_list));
	#print "vertices: {0}".format(len(vertices));
	rank = GF2_matrix_rank(matrix, len(edge_list), len(triangle_set));
	return len(edge_list) - len(vertices) + 1 - rank;


class Component:
	'''Define a 'component' as a set of spheres, such that there is no 1-d holes.
	meaning the first betti number is 0 '''
	def __init__(self, init_ball = None):
		'''A component should at least have one ball'''
		self.spheres = {}
		if init_ball != None:
			self.spheres[init_ball] = 1;
		self.edge_set = {};
		self.triangle_set = {};

	def construct(self, spheres, edge_tri_dict, sphere_tri_dict):
		'''given a set of spheres, construct a component'''
		self.spheres = spheres;
		for v1, v2 in edge_tri_dict.keys():
			if spheres.has_key(v1) and spheres.has_key(v2):
				self.edge_set[(v1, v2)] = 1;

		for s in spheres.keys():
			tris = sphere_tri_dict[s];
			for tri in tris:
				if self.spheres.has_key(tri.spheres[0]) and self.spheres.has_key(tri.spheres[1]) and self.spheres.has_key(tri.spheres[2]):
					self.triangle_set[tri] = 1;

		return;


	def get_spheres(self):
		return self.spheres.keys();

	def intersects(self, sphere):
		'''determine if a sphere intersects with current component'''
		if self.spheres.has_key(sphere):
			return False;
		for s in self.spheres.keys():
			if s.intersects(sphere):
				return True;
		return False;

	def betti_number(self, edge_tri_dict):
		return betti_number(self.triangle_set, self.edge_set.keys(), edge_tri_dict);

	def __new_tirsNedges__(self, sphere, edge_tri_dict, sphere_tri_dict):
		if not self.intersects(sphere):
			return None, None;

		new_triangles = {};
		new_edges = {};
		self.spheres[sphere] = 1;

		candidate_triangles = sphere_tri_dict[sphere];
		i = 1;
		for tri in candidate_triangles:
			if new_triangles.has_key(tri) and self.triangle_set.has_key(tri):
				continue;
			# all vertices in the triangle are in the component;
			valid = True;
			for s in tri.spheres:
				if not self.spheres.has_key(s):
					valid = False;
			if not valid:
				continue;
			new_triangles[tri] = 1;

			# add edges of the triangle to our component
			for v1, v2 in tri.edges():
				if (not self.edge_set.has_key((v1, v2)) and not self.edge_set.has_key((v2, v1))) and ( not new_edges.has_key( (v2, v1)) and not new_edges.has_key( (v2, v1) ) ):
					new_edges[ (v1, v2) ] = 1;
					#pygame.draw.line( surf, (255,0,0), (int(v1.center[0]),int(v1.center[1])), (int(v2.center[0]),int(v2.center[1])), 2 )
					#pygame.display.update();

		# Get new edges that might be added to the component
		for ball in self.spheres.keys(): 			# This step could be slow!!! (If the component has too many spheres already)
			if ball.intersects(sphere) and not new_edges.has_key((ball, sphere)) and not new_edges.has_key((sphere,ball)):
				if edge_tri_dict.has_key( (ball, sphere) ) or edge_tri_dict.has_key((sphere, ball)):
					new_edges[(ball, sphere)] = 1;
					#pygame.draw.line( surf, (255,0,0), (int(ball.center[0]),int(ball.center[1])), (int(sphere.center[0]),int(sphere.center[1])), 2 )
					#pygame.display.update();

		del self.spheres[sphere];

		print "Add {0} new triangles".format(len(new_triangles))
		return new_edges, new_triangles;

	def merge(self, other, edge_tri_dict, sphere_tri_dict):
		'''merge two components, the 1st betti number doesn't hanve to be 0 any more.'''
		#total_spheres = dict(self.spheres.items() + other.spheres.items());
		#total_edge_set = dict( self.edge_set.items());
		#total_triangle_set = dict( self.triangle_set.items());
		print "self spheres: {0} \t other spheres: {1}".format(len(self.get_spheres()), len(other.get_spheres()));

		total_spheres = merge_sets(self.spheres, other.spheres);
		#total_edge_set = dict( self.edge_set.items() + other.edge_set.items());
		#total_triangle_set = dict( self.triangle_set.items() + other.triangle_set.items());
		

		new_comp = Component()
		new_comp.construct(total_spheres, edge_tri_dict, sphere_tri_dict)
		#new_comp.spheres = total_spheres;
		#new_comp.triangle_set = total_triangle_set;
		#new_comp.edge_set = total_edge_set;
		
		print "Merged Total Triangles: {0}".format(len(new_comp.triangle_set.keys()))
		print "Merged Total Spheres: {0}".format(len(new_comp.spheres.keys()))
		print "Self Betti number: {0}".format( self.betti_number(edge_tri_dict) )
		print "Other Betti number: {0}".format( other.betti_number(edge_tri_dict) )
		print "Merged Betti number: {0}".format( new_comp.betti_number(edge_tri_dict) )

		return new_comp;

	def remove_sphere(self, sphere, old_betti, edge_tri_dict, sphere_tri_dict, force = False):
		rmed_edges = [];
		rmed_tris  = [];
		del self.spheres[sphere];			# delete sphere
		for edge in self.edge_set.keys():	# delete edge with sphere as a vertex
			if edge[0] == sphere or edge[1] == sphere:
				rmed_edges.append(edge);
				del self.edge_set[edge];

		for tri in self.triangle_set.keys():# delete triangle that contains the sphere
			if sphere in tri.spheres:
				rmed_tris.append(tri);
				del self.triangle_set[tri];

		if self.betti_number(edge_tri_dict) > old_betti and not force:   # If it increases the betti number and is not forced to remove the sphere
			for edge in rmed_edges:				# add edges back
				self.edge_set[edge] = 1;
			for tri in rmed_tris:				# add triangles back
				self.triangle_set[tri] = 1;
			self.spheres[sphere] = 1;			# add sphere back
			return False;
		else:
			return True; 

	def remove_spheres(self, untouchable, edge_tri_dict, sphere_tri_dict, surf ):
		print "========== Start Removing spheres ==========="
		# Get original betti number
		betti = self.betti_number(edge_tri_dict);
		print 'Original betti {0}'.format(betti)
		remove_one = True;   # If we can remove one sphere
		while betti > 0 and remove_one:
			remove_one = False;
			for sphere in self.spheres.keys():
				if betti == 0:
					return betti
				if untouchable.has_key(sphere) :   # don't touch untouchable spheres
					continue;
				if not self.spheres.has_key(sphere): # already removed
					continue;
				pygame.draw.circle(surf, (0,0,255), (int(sphere.center[0]), int(sphere.center[1])), int(sphere.radius));
				pygame.display.update()
				time.sleep(0.3)
				if self.remove_sphere(sphere, betti, edge_tri_dict, sphere_tri_dict):
					betti = self.betti_number(edge_tri_dict);
					print betti
					remove_one = True;
					pygame.draw.circle(surf, (255,255,255), (int(sphere.center[0]), int(sphere.center[1])), int(sphere.radius));
					pygame.display.update();
					time.sleep(0.3);
		return betti;

	def add_sphere(self, sphere, edge_tri_dict, sphere_tri_dict, surf=None):
		return self.add_sphere_betti(sphere, 0, edge_tri_dict, sphere_tri_dict, surf);

	def add_sphere_betti(self, sphere, old_betti, edge_tri_dict, sphere_tri_dict, surf=None):
		'''determine if we can add a sphere to the component without increasing the 1-st betti number'''
		if self.spheres.has_key(sphere):
			return False;
			#raise Exception('You got a bug, the sphere is already in the component');
		self.spheres[sphere] = 1;
		
		new_triangles = {};
		new_edges = {};

		candidate_triangles = sphere_tri_dict[sphere];
		i = 1;
		for tri in candidate_triangles:
			if new_triangles.has_key(tri) and self.triangle_set.has_key(tri):
				continue;
			# all vertices in the triangle are in the component;
			valid = True;
			for s in tri.spheres:
				if not self.spheres.has_key(s):
					valid = False;
			if not valid:
				continue;
			new_triangles[tri] = 1;
			draw_triangle(tri, surf, (0,250,0));
			pygame.display.update();

			# add edges of the triangle to our component
			for v1, v2 in tri.edges():
				if (not self.edge_set.has_key((v1, v2)) and not self.edge_set.has_key((v2, v1))) and ( not new_edges.has_key( (v2, v1)) and not new_edges.has_key( (v2, v1) ) ):
					new_edges[ (v1, v2) ] = 1;
					pygame.draw.line( surf, (255,0,0), (int(v1.center[0]),int(v1.center[1])), (int(v2.center[0]),int(v2.center[1])), 2 )
					pygame.display.update();

		# Get new edges that might be added to the component
		for ball in self.spheres.keys(): 			# This step could be slow!!! (If the component has too many spheres already)
			if ball.intersects(sphere) and not new_edges.has_key((ball, sphere)) and not new_edges.has_key((sphere,ball)):
				if edge_tri_dict.has_key( (ball, sphere) ) or edge_tri_dict.has_key((sphere, ball)):
					new_edges[(ball, sphere)] = 1;
					pygame.draw.line( surf, (255,0,0), (int(ball.center[0]),int(ball.center[1])), (int(sphere.center[0]),int(sphere.center[1])), 2 )
					pygame.display.update();
		
		#new_edges, new_triangles = self.__new_tirsNedges__(sphere, edge_tri_dict, sphere_tri_dict);

		# Now we have distinct new edges and new triangles while add a new sphere
		# Add them up.
		total_triangle_set = dict(self.triangle_set.items() + new_triangles.items());
		total_edges 	   = dict(self.edge_set.items() + new_edges.items());
		# Time to determine the betti number.
		#print "Total Triangle Set:\n {0}".format(total_triangle_set);
		#print "Total Edge Set: {0}".format(total_edges);
		#print "Total spheres:\n{0}".format( self.spheres );
		betti 	   		   = betti_number(total_triangle_set, total_edges.keys(), edge_tri_dict);

		if betti <= old_betti:				# If it will not increase the 1-st betti number
			self.spheres[sphere] = 1;		# add the sphere to the component
			self.triangle_set = total_triangle_set;# update triangles in the component
			self.edge_set     = total_edges;	# update edges in the component.
			return True;					# Tell caller the sphere can be added to the component
		del self.spheres[sphere];
		return False;						# Tell caller the sphere cannot be added to the component

	def render(self, surf, color):
		for sphere in self.get_spheres():
			pygame.draw.circle( surf, color, (int(sphere.center[0]), int(sphere.center[1])), int(sphere.radius), 2 );
		
		for triangle in self.triangle_set.keys():
			points = [ (int(triangle.spheres[0].center[0]), int(triangle.spheres[0].center[1]) ), (int(triangle.spheres[1].center[0]), int(triangle.spheres[1].center[1]) ), ( int(triangle.spheres[2].center[0]), int(triangle.spheres[2].center[1] )) ];
			pygame.draw.polygon(surf, color, points, 2);

		for v1, v2 in self.edge_set.keys():
			p1 = ( int(v1.center[0]), int(v1.center[1]) )
			p2 = ( int(v2.center[0]), int(v2.center[1]) )
			pygame.draw.line(surf, color, p1, p2, 3);
		pass;	

class Contraction:
	def __init__(self, spheres, surface):
		self.spheres = spheres;
		self.surface = surface;
		self.graph = {};			# connections between spheres

		for sphere1 in self.spheres:
			if not self.graph.has_key(sphere1):
				self.graph[sphere1] = [];
			for sphere2 in self.spheres:
				if sphere1 != sphere2 and sphere1.intersects(sphere2):
					if not sphere2 in self.graph[sphere1]:
						self.graph[sphere1].append(sphere2);

	def contract(self, triangle_set, edge_tri_dict, sphere_tri_dict):
		'''Contract a set of balls to several sets of balls, such that each set has first betti number of 0'''
		used_spheres = {}
		component_set = [];

		for sphere in self.spheres:					# Loop over all spheres 
			if not used_spheres.has_key(sphere):	# make sure the sphere is not used
				# Create a component starting from this sphere.
				component = self.contract_sphere(sphere, used_spheres, edge_tri_dict, sphere_tri_dict)
				component_set.append(component)

		return component_set;

	def contract_sphere(self, sphere, used_spheres, edge_tri_dict, sphere_tri_dict):
		'''start from a sphere as the init of component, contract its neighbors as much as possible'''
		component = Component(sphere);					# Start from the initial sphere
		used_spheres[sphere] = 1;
		print '---------------------------------------------'
		print sphere
		find_new_sphere = True;							# Mark if we keep finding new spheres

		skip_spheres = {}								# Some spheres will increase the betti number,
														# we store them here such that they don't have to be tried very round
		skip_sphere_attemps = {}						# attemps for adding a skip sphere

		while find_new_sphere:							# Loop until we can't find any new spheres to add
														# Find all neighbor spheres ( such that they are not used in any components )
			neighbors = self.component_neighbor_spheres(component, used_spheres, sphere_tri_dict);  
			find_new_sphere = False;
			for neighbor in neighbors:								# Loop over each neighbor sphere
				if used_spheres.has_key(neighbor):
					continue;
				if skip_spheres.has_key(neighbor) and skip_spheres[neighbor] != 0:
					skip_spheres[neighbor] = skip_spheres[neighbor]-1;
					find_new_sphere = True;
					print "Skip update: {0} \t\t {1}".format( neighbor, skip_spheres[neighbor] )
					continue;
				pygame.draw.circle( self.surface, (250,0,0), (int(neighbor.center[0]), int(neighbor.center[1])), int(neighbor.radius), 2 );
				pygame.display.update();
				#time.sleep(0.5)
				#print "testing {0}".format(neighbor);
				if component.add_sphere(neighbor, edge_tri_dict, sphere_tri_dict, self.surface):	# if it can be added to the current component, add it.
					used_spheres[neighbor] = 1;						# mark the sphere as used
					find_new_sphere = True;							# Yes, we've found a new sphere. Keep looping.
					print "Good!"
					component.render(self.surface, (0,250,0));
					pygame.draw.circle( self.surface, (0,250,0), (int(neighbor.center[0]), int(neighbor.center[1])), int(neighbor.radius), 2 );
					pygame.display.update();
				else:
					if not skip_sphere_attemps.has_key(neighbor):
						skip_sphere_attemps[neighbor] = 1;
						skip_spheres[neighbor] = skip_sphere_attemps[neighbor] * 2;
						print "Skip update: {0} \t\t {1}".format( neighbor, skip_spheres[neighbor] )
					else:
						skip_sphere_attemps[neighbor] += 1;
						skip_spheres[neighbor] = skip_sphere_attemps[neighbor] * 2;
						print "Skip update: {0} \t\t {1}".format( neighbor, skip_spheres[neighbor] )


				#time.sleep(1);

		return component;

	def component_neighbor_spheres(self, component, used_spheres, sphere_tri_dict):
		'''Find component's neighbor spheres'''
		comp_spheres = component.get_spheres();	# spheres belong to the component
		neighbors = [];							# neighbor spheres of the component.
		for sphere in comp_spheres:				# loop over each component sphere
			curr_neighbors = self.graph[sphere];# find its neighbors in the graph
			for curr_neighbor in curr_neighbors:
				if not used_spheres.has_key(curr_neighbor): # such that each neighbor is not used
					neighbors.append(curr_neighbor);
		return neighbors;