
"""
This class is about determine two path homotopy classes using Constraint Satisfication Programming techniques.+
"""

__author__ = 'Yinan Zhang'
__revision__ = '$Revision$'

import pdb
import sys, os, math, time, pygame, time, copy
sys.path.append('../basics/math')
sys.path.append('../basics/algorithm')

from numpy.linalg 	import matrix_rank
from hyper_geometry import *
from l1_geometry	import *
from Triangle		import *
from Contraction 	import *
from priority_queue import *

class HomotopyCSP:
	'''Constraint Satisfication Programming on homotopy of sphere unions'''
	def __init__(self, spheres, graph, triangle_set, edge_tri_dict, sphere_tri_dict):
		self.spheres 		= spheres
		self.graph 			= graph
		self.triangle_set 	= triangle_set
		self.edge_tri_dict 	= edge_tri_dict
		self.sphere_tri_dict = sphere_tri_dict
		pass;

	def neighbor_spheres( self, union, used_spheres ):
		for sphere in union.get_spheres():
			used_spheres[sphere] = 1;

		neighbors = [];							# neighbor spheres of the union.
		for sphere in union.get_spheres():				# loop over each component sphere
			curr_neighbors = self.graph[sphere];# find its neighbors in the graph
			for curr_neighbor in curr_neighbors:
				if not used_spheres.has_key(curr_neighbor): # such that each neighbor is not used
					neighbors.append(curr_neighbor);
		print "Union neighbor spheres: {0}".format( len(neighbors) );
		return neighbors;

	def greedy( self, union1, union2, surface = None ):

		def dist(sphere, union):
			'''min_dist from a sphere to spheres on a union'''
			min_dist = 100000000;
			for s in union.get_spheres():
				dist = (s.center - sphere.center).r();
				if dist <= min_dist:
					min_dist = dist;
			return min_dist;

		
		union1.render( surface, (200,200,200) );	union2.render( surface, (200,000,200) );
		pygame.display.update();
		used_spheres = {};
		for sphere in union1.get_spheres():
			used_spheres[sphere] = 1;

		for sphere in union2.get_spheres():
			used_spheres[sphere] = 1;
		
		union1cp = copy.copy( union1 );
		union = union1cp.merge(union2, self.edge_tri_dict, self.sphere_tri_dict);
		neighbors = self.neighbor_spheres(union1, used_spheres)
		heuristic = PriorityQueue();
		

		if len(neighbors) == 0:
			pass;   #### Think about this
		for neighbor in neighbors:
			heuristic.push( neighbor, dist(neighbor, union1) + dist(neighbor, union1) );

		while not heuristic.isEmpty():
			choice = heuristic.pop()
			print choice
			pygame.draw.circle( surface, (255,0,0), (int(choice.center[0]), int(choice.center[1])), int(choice.radius), 2 );
			pygame.display.update()
			time.sleep(1);
			old_betti = union.betti_number(self.edge_tri_dict)
			print "old betti number: {0}".format( old_betti )
			good = union.add_sphere_betti(choice, old_betti, self.edge_tri_dict, self.sphere_tri_dict, surface);
			if good == None:
				print "Same homotopy class";
				return;
			if good:
				union.render( surface, (200,200,200) );
				time.sleep(1);
				used_spheres[choice] = 1;
				temp = Component( choice );
				new_neighbors = self.neighbor_spheres(temp, used_spheres)
				for neighbor in new_neighbors:
					heuristic.push( neighbor, dist(neighbor, union1) + dist(neighbor, union1) );
					break;
			else:

				heuristic.push( choice, dist(choice, union1) + dist(choice, union1) );
			
		betti = union.betti_number(self.edge_tri_dict);
		print betti
		if betti != 0:
			print "Different Homotopy Classes"
		else:
			print "Same homotopy class"


