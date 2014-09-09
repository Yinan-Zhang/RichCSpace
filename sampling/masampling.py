
import sys,os,math

sys.path.append('../basics/math')
sys.path.append('../basics/robotics')

from geometry import *
from configuration import *
from robot import *
from BlockRobot import *

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
			raise Exception('Please give a BlockRobotConfig instance');
		return robot.is_valid_config( config )

	def config_clearance( self, robot, config, mode = 'L2' ):
		'''get the config clearance with L2 metric'''
		if not isinstance(robot, BlockRobot):
			raise Exception( 'Please give a BlockRobot instance' );
		if not isinstance(config, BlockRobotConfig):
			raise Exception('Please give a BlockRobotConfig instance');
		return robot.config_clearance(config, mode);

	def maSample(self, robot, config, direction, max_len):
		'''get the medial axis sample along a directon, with max length'''
		if not self.is_valid_config(robot, config):
			raise Exception('Has to be a feasible configuration');
		t = 1;
		last_increase = False;
		last_dist = self.config_clearance(robot, config);
		this_increase = ((this_dist-last_dist)>0);
		while True:
			temp = config + direction * t
			this_dist = self.config_clearance(robot, config);
			if last_dist and not this_increase:
				if not self.is_valid_config(robot, temp):
					return temp, this_dist;
				else:
					return None, None;
			else:
				t += 1;
				last_increase = this_increase;
				last_dist = this_dist;

			if t-1 >= max_len:
				break;

		return None, None;

class MedialAxisSampling:
	'''sampling on medial axis'''
	def __init__(self, robot, helper ):
		if not isinstance(robot, Robot):
			raise Exception( 'Please give a Robot instance' );
		if not isinstance(helper, samplinghelper):
			raise Exception('Please give a samplinghelper instance');
		self.robot = robot;
		self.helper = helper;

	def sample_medial_axis(self, randSamples):
		'''Given a bunch of random samples, find some medial axis samples using them'''
		length = 40;
		ma_samples = []

		for config in randSamples:
			

