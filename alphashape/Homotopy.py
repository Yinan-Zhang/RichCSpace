
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

	def greedy( self, union1, union2, all_spheres, surface = None ):
		''' Greedily grow spheres for a set of balls two paths go through, 
		such that the growth will not increase the 1st betti number.
		'''

		def center( union1, union2 ):
			center = None;
			for s in union1.spheres:
				if center is None:
					center = copy.copy( s.center );
				else:
					center += s.center;
			for s in union2.spheres:
				center += s.center;

			center /= ( len(union1.spheres) + len(union2.spheres) );
			return center;

		def dist(sphere, union):
			'''min_dist from a sphere to spheres on a union'''
			min_dist = 100000000;
			for s in union.get_spheres():
				dist = (s.center - sphere.center).r();
				if dist <= min_dist:
					min_dist = dist;
			return min_dist;

		def heur_dist( sphere, union1, union2 ):
			'''returns the heuristic of the sphere'''
			return dist(sphere, union1) + dist(sphere, union2);

		def heur_cent( sphere, center ):
			'''returns the heuristic of the sphere'''
			return (sphere.center - center).r();

		pdb.set_trace();

		union_center = center(union1, union2);
		union1.render( surface, (200,200,00) );	
		pygame.display.update();
		union2.render( surface, (200,000,200) );
		pygame.display.update();
		used_spheres = {};
		for sphere in union1.get_spheres():
			used_spheres[sphere] = 1;

		for sphere in union2.get_spheres():
			used_spheres[sphere] = 1;
		
		union1cp = copy.copy( union1 );
		union = union1.merge(union2, self.edge_tri_dict, self.sphere_tri_dict);
		neighbors = self.neighbor_spheres(union, used_spheres)
		heuristic = PriorityQueue();

		if len(neighbors) == 0:
			pass;   ####sThink about this
		for neighbor in neighbors:
			if not used_spheres.has_key(neighbor) and all_spheres.has_key(neighbor):
				heuristic.push( neighbor, heur_dist(neighbor, union1, union2) );
				#heuristic.push(neighbor, heur_cent(neighbor, union_center));

		pdb.set_trace();
		while not heuristic.isEmpty() and not len(union.spheres) == len(all_spheres.keys()):
			choice = heuristic.pop()
			
			pygame.draw.circle( surface, (255,0,0), (int(choice.center[0]), int(choice.center[1])), int(choice.radius), 2 );
			pygame.display.update()
			#time.sleep(1);
			old_betti = union.betti_number(self.edge_tri_dict)
			print "old betti number: {0}".format( old_betti )
			good = union.add_sphere_betti(choice, old_betti, self.edge_tri_dict, self.sphere_tri_dict, surface);
			if old_betti == 0 or good == None:
				print "Same homotopy class";
				return;
			if good:
				union.render( surface, (200,200,200) );
				time.sleep(1);
				used_spheres[choice] = 1;
				temp = Component( choice );
				new_neighbors = self.neighbor_spheres(temp, used_spheres)
				for neighbor in new_neighbors:
					if not used_spheres.has_key(neighbor) and all_spheres.has_key(neighbor):
						heuristic.push( neighbor, heur_dist(neighbor, union1, union2) );
						#heuristic.push(neighbor, heur_cent(neighbor, union_center));
			
		betti = union.betti_number(self.edge_tri_dict);
		print betti
		if betti != 0:
			print "Different Homotopy Classes"
		else:
			print "Same homotopy class"


	def CSP( self, all_spheres, path1, path2, surf ):
		'''Given n variables( spheres ) s[1..n] with available value 0 and 1. 
		Solve the constraint satisfication problem of assigning variables such that:
		1. either the assigned spheres have betti number 0
		2. or there's no other spheres that can be added without increasing the betti number'''
		path1cp = copy.copy(path1);
		component = path1cp.merge(path2, self.edge_tri_dict, self.sphere_tri_dict);
		assigned = {}
		for s in component.spheres.keys():
			assigned[s] = 1;

		return self.CSP_helper(all_spheres, assigned, component, surf)


	def CSP_helper( self, all_spheres, assigned, component, surf ):
		
		def dist(sphere, ball):
			'''min_dist from a sphere to spheres on a union'''
			min_dist = 100000000;
			for s in union.get_spheres():
				dist = (s.center - sphere.center).r();
				if dist <= min_dist:
					min_dist = dist;
			return min_dist;

		def heur( sphere, path1, path2 ):
			'''returns the heuristic of the sphere'''
			return dist(sphere, union1) + dist(sphere, union2);

		def select_next_unassigned(idx):
			'''returns the an unassigned variable'''
			spheres = all_spheres.keys();
			for i in range(idx, len(spheres)):
				s = spheres[i]
				if not assigned.has_key(s) and component.intersects(s):
					idx += 1;
					return s, idx;
				idx += 1;

			return None;

		pdb.set_trace();
		old_betti = component.betti_number( self.edge_tri_dict );
		print old_betti
		if old_betti == 0:
			return True; # Same homotopy

		idx = 0;
		while True:
			pdb.set_trace()
			component.render(surf, (150, 180, 230));
			pygame.display.update();
			var, idx = select_next_unassigned(idx);
			if var == None:
				return False;
			if component.add_sphere_betti(var, old_betti, self.edge_tri_dict, self.sphere_tri_dict, surf):
				component.render(surf, (150, 180, 230));pygame.display.update();
				assigned[var] = 1;
				if not self.CSP_helper(all_spheres, assigned, component, surf):
					component.remove(var, old_betti, self.edge_tri_dict, self.sphere_tri_dict, True);
				else:
					return True;
		pass;