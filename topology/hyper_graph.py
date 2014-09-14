
'''
Hyper graph
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

import sys, os, copy
sys.path.append('../basics/math')
sys.path.append('../alphashape')

from l1_geometry 		import *
from hyper_geometry 	import *
from hyper_alpha_shape 	import *

class Graph:
	def __init__(self, dictionary = None):
		'''Graph described by a dictionary.
		A graph is of this format:

        {
        	'A' : ['B','C'],
        	'B' : ['A','C'],
        	'C' : ['A','B']
        }

       	     
        A ------- B
         \       /
          \     /  
           \   /
             C 
		'''
		self.graphdict = dictionary;

	def adj_nodes_of(self, node):
		return self.graphdict[node];
		
	def all_nodes(self):
		'''get all nodes in the graph'''
		return self.graphdict.keys();

	def size(self):
		return len(self.all_nodes());

	def share_nodes_with(self, other):
		'''determine if two graphs share same ndoes'''
		othernodes = other.get_all_nodes();
		for node in othernodes:
			if self.graphdict.has_key( node ):
				return True;
		return False;

	def num_of_loops(self):
		'''the number of 1d holes'''
		edge_num = 0;
		for node in self.graphdict.keys():
			neighbors = self.graphdict[node];
			edge_num += len(neighbors);
		edge_num /= 2;
		vert_num = len(self.graphdict.keys());
		return edge_num - vert_num + 1;

	def find_all_paths(self, start, end, path=[]):
		path = path + [start];
		if start == end:
			return [path];
		if not self.graphdict.has_key(start) or not self.graphdict.has_key(end):
			return [];
		paths = [];
		for neighbor in self.graphdict[start]:
			if neighbor not in path:
				newpaths = self.find_all_paths( node, end, path);
				for newpath in newpaths:
					paths.append(newpath);
		return paths;

