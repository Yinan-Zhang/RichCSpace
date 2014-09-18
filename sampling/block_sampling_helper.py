import sys,os,math,random

sys.path.append('../basics/math')
sys.path.append('../basics/robotics')

from geometry 		import *
from hyper_geometry import *
from configuration 	import *
from robot 			import *
from BlockRobots 	import *
from masampling 	import *
from l1_geometry 	import *

class BlockSamplingHelper( samplinghelper ):
	def __init__(self):
		samplinghelper.__init__(self);
		pass;

	def is_valid_config( self, robot, config ):
		if not isinstance(robot, BlockRobot):
			raise Exception( 'Please give a BlockRobot instance' );
		if not isinstance(config, BlockRobotConfig):
			config = BlockRobotConfig(config[0], config[1], config[2], config[3]);
		return robot.is_valid_config( config )

	def config_clearance( self, robot, config, dimensions, mode = 'L2' ):
		'''get the config clearance with L2 metric.
		@param dimensions: max values of each dimension'''
		if not isinstance(robot, BlockRobot):
			raise Exception( 'Please give a BlockRobot instance' );
		if not isinstance(config, BlockRobotConfig):
			config = BlockRobotConfig(config[0], config[1], config[2], config[3]);
		return robot.config_clearance(config, mode);

	def maSample(self, robot, config, direction, max_len, dimensions, mode = 'L2'):
		'''get the medial axis sample along a directon, with max length.
		@param dimensions: max values of each dimension'''
		if not self.is_valid_config(robot, config):
			#raise Exception('Has to be a feasible configuration');
			return None, None
		t = 1;
		last_increase = False;
		last_dist = self.config_clearance(robot, config, dimensions, mode);
		dists = [last_dist];
		while True:
			if t-1 >= max_len:
				return None, None;
			temp = config + direction * t
			#print temp
			this_dist = self.config_clearance(robot, temp, dimensions, mode); 
			dists.append(this_dist);
			if (last_dist > 0 and this_dist <=0):
				break;
			this_increase = ((this_dist-last_dist)>0);
			if last_increase and not this_increase:
				if self.is_valid_config(robot, temp):
					#print '-----------------------------'
					#print dists
					return temp, this_dist;
				else:
					return None, None;
			else:
				t += 1;
				last_increase = this_increase;
				last_dist = this_dist;

		return None, None;