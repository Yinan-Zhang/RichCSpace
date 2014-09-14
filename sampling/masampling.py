
import sys,os,math,random

sys.path.append('../basics/math')
sys.path.append('../basics/robotics')

from geometry 		import *
from hyper_geometry import *
from configuration 	import *
from robot 			import *
from BlockRobots 	import *
from l1_geometry 	import *

class Sample():
	'''A sample is a configuration with clearance. '''
	def __init__( self, center, radius, mode ):
		self.mode = mode;
		if mode == 'L1' or mode == 'l1':
			self.sphere = l1_sphere(center, radius);
		elif mode == 'L2' or mode == 'l2':
			self.sphere = hyper_sphere(center, radius);
		#hyper_sphere.__init__(self,center, radius);
		self.rnd_cfgs = []; 					# Random configurations 
		self.bnd_cfgs = [];						# boundary configurations
		self.closed = False;
		self.center = self.sphere.center;
		self.radius = self.sphere.radius;

	def contains( self, point ):
		'''determine if the point is inside the sphere
		@param point: (vec) the point'''
		return self.sphere.contains(point);

	def intersects( self, other ):
		'''determine if the other sphere is intersecting with self'''
		return self.sphere.intersects(other.sphere);

	def distance(self, point):
		'''distance from a point to the boundary of the sphere'''
		if self.mode == 'L2' or self.mode == 'l2':
			centerdist = (point - self.center).r();
		elif self.mode == 'L1' or self.mode == 'l1':
			centerdist = (point - self.center).l1()
		return centerdist - self.radius;

	def add(self, point):
		'''if the point is inside it, add it to the rnd_cfgs set.'''
		if not self.contains(point):
			return False;
		if self.__closed__:
			return True;
		self.rnd_cfgs.append( point );
		return True;

	def boundary_configs(self):
		'''Push all configs to the boundary of the sphere'''
		if self.bnd_cfgs is not None:
			return self.bnd_cfgs;
		self.bnd_cfgs = [];
		for point in self.rnd_cfgs:
			dir = (point - self.center);
			if dir.r() == 0:
				dir = v2(1,3);
			dir = dir.normalize();
			bnd_cfg = self.center + dir * (self.radius+0.5);
			self.bnd_cfgs.append( bnd_cfg );

		#self.rnd_cfgs = [];
		return self.bnd_cfgs;

class samplinghelper:
	def __init__( self ):
		pass;

	def is_valid_config( self, robot, config ):
		'''determine if a config is feasible'''
		pass;

	def config_clearance( self, robot, config, mode = 'L2' ):
		'''Get the config clearance'''
		pass;

	def maSample( self, robot, config, direction ):
		'''get the medial axis sample along a direction'''
		pass;

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

class MedialAxisSampler:
	'''sampling on medial axis'''
	def __init__(self, robot, helper ):
		if not isinstance(robot, Robot):
			raise Exception( 'Please give a Robot instance' );
		if not isinstance(helper, samplinghelper):
			raise Exception('Please give a samplinghelper instance');
		self.robot = robot;
		self.helper = helper;

	def random_invalid_configs(self, dim, num, dimensions):
		'''get a number of random invalid configurations in dim-dimensional space
		@param dimensions: max values of each dimension'''
		rnd_cfgs = []

		for i in range(0, num):
			cfg = [0]*dim;
			cfg[0] = cfg[1] = 400.0;
			for j in range(2, dim):
				cfg[j] = float(random.randint( 0, dimensions[j] ));
			if not self.helper.is_valid_config(self.robot, cfg):
				rnd_cfgs.append( Config(cfg) );
			else:
				i -= 1;

		return rnd_cfgs;

	def random_configs(self, dim, num, dimensions):
		'''get a number of random configurations in dim-dimensional space
		@param dimensions: max values of each dimension'''
		rnd_cfgs = []

		for i in range(0, num):
			cfg = [0]*dim;
			cfg[0] = cfg[1] = 400.0;
			for j in range(2, dim):
				cfg[j] = float(random.randint( 0, dimensions[j] ));
			if self.helper.is_valid_config(self.robot, cfg):
				rnd_cfgs.append( Config(cfg) );
			else:
				i -= 1;

		return rnd_cfgs;

	def random_dir(self, dim):
		'''get a random dirtion in dim-dimensional space.
		'''
		dir = vec([0]*dim);
		dir[0] = dir[1] = 0.0;
		for i in range(2, dim):
			dir[i] = float(random.randint( -100, 100 ));

		if dir.r() == 0:
			dir = vec( [1]*dim );

		return dir.normalize();

	def sample_medial_axis(self, randSamples, dimensions, mode = 'L2'):
		'''Given a bunch of random samples, find some medial axis samples using them.
		@param dimensions: max values of each dimension'''
		length = 30;
		ma_samples = []

		for config in randSamples:
			'''
			good = True;
			for sphere in ma_samples:
				if sphere.contains(config):
					good = False;
					break;
			if not good:
				continue;
			'''
			rnd_dir = self.random_dir( len(config) );
			center, clearance = self.helper.maSample(self.robot, config, rnd_dir, length, dimensions, mode);
			if clearance == None or clearance <= 5.0:
				continue;
			sample = Sample(center, clearance, mode,);
			good = True;
			for sphere in ma_samples:
				if sphere.contains(sample.center):
					good = False;
					break;

			if good:
				ma_samples.append(sample);

		return ma_samples;


	def save_data( self, samples, filename ):
		'''Save sampled spheres. Write data to a file'''
		file2write = open( filename, 'w' );
		formattedData = "";
		for sphere in samples:
			for i in range(0, len(sphere.center)):
				formattedData += str( sphere.center[i] ) + "\t";
			formattedData += str( sphere.radius);
			formattedData += "\n";

		file2write.write( formattedData );
		file2write.close();
