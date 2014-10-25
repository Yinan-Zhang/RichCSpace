'''
Given a set of sphere samples that almost cover the free space. 
We want to make sure that no 1d hole are generated because of sampling.
That is we will not increase 1st betti number becuse of no enough samples.
'''

import sys, os, math, copy, pygame

sys.path.append('../')
sys.path.append('../../basics/math')
sys.path.append('../../basics/robotics')


from geometry 		import *
from hyper_geometry import *
from configuration 	import *
from robot 			import *
from BlockRobots 	import *
from l1_geometry 	import *
from Triangulator 	import *

class DetailSampler(MedialAxisSampler):
	def detail_sample( self, randSamples, dimensions, mode = 'L2' ):
		masamples = self.sample_medial_axis(self, randSamples, dimensions, mode)
		triangulator = Triangulator(masamples);
		triangle_set, sphere_tri_dict, edge_tri_dict = triangulator.triangulate();

		