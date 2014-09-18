import sys,os,math,random

sys.path.append('../basics/math')
sys.path.append('../basics/robotics')

from geometry 		import *
from hyper_geometry import *
from configuration 	import *
from robot 			import *
from WarehouseRobot import *
from masampling 	import *
from l1_geometry 	import *

class WarehouseSamplingHelper( samplinghelper ):
	def __init__(self):
		samplinghelper.__init__(self);
		pass;

	def is_valid_config( self, robot, config ):
		if not isinstance(robot, WarehouseRobot):
			raise Exception( 'Please give a BlockRobot instance' );
		if not isinstance(config, Config):
			config = Config([config[0], config[1]]);
		return robot.is_valid_config( config )

	def config_clearance( self, robot, config, dimensions, mode = 'L2' ):
		'''get the config clearance with L2 metric.
		@param dimensions: max values of each dimension'''
		if not isinstance(robot, WarehouseRobot):
			raise Exception( 'Please give a BlockRobot instance' );
		if not isinstance(config, Config):
			config = Config([config[0], config[1]]);
		return robot.config_clearance(config, mode);

	def __rand_dir__(self, dim):
		'''get a random dirtion in dim-dimensional space.'''
		dir = vec([0]*dim);
		dir[0] = dir[1] = 0.0;
		for i in range(0, dim):
			dir[i] = float(random.randint( -100, 100 ));

		if dir.r() == 0:
			dir = vec( [1.0]*dim );

		return dir.normalize();

	def __find_max_dir__(self, robot, config, dimensions, mode ='L2'):
		'''Find the direction with the max increment of clearance'''
		n = 100;
		dim = len(dimensions);

		max_dir = None;
		max_clearance = 0;
		for i in range(0,n):
			rand_dir = self.__rand_dir__(dim);
			rand_cfg = config + rand_dir * 2.0;
			clearance = self.config_clearance(robot, rand_cfg, dimensions);
			if clearance > max_clearance:
				max_clearance = clearance;
				max_dir = rand_dir;

		return max_dir;

	def __naive_sampling__(self, robot, config, direction, max_len, dimensions, mode = 'L2'):
		pass;

	def maSample( self, robot, config, direction, max_len, dimensions, mode = 'L2' ):
		max_dir = self.__find_max_dir__(robot, config, dimensions);
		return samplinghelper.maSample(self, robot, config, max_dir, 80, dimensions, mode );
