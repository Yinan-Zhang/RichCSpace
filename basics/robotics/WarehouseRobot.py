import sys, os, copy
sys.path.append('../math')

import pygame;
import math;

from geometry import *
from polygon import *
from hyper_geometry import *
from configuration import *
from robot import *
from BlockRobots import Block

class WarehouseRobot( Robot ):
	def __init__(self, dimensions):
		'''@param dimensions: world dimensions.'''
		self.dimensions = dimensions;
		points = [ v2(0,0), v2(200,0), v2(200,100), v2(0,100) ];
		self.blocks = [];
		self.robot = sphere2d(v2(0.0,0.0), 15.0);
		block = Block(points);
		for i in range(0,6):
			block_i = copy.deepcopy(block);
			self.blocks.append(block_i);
		self.blocks[0].translate( v2(100, 100) );
		self.blocks[1].translate( v2(500, 100) );
		self.blocks[2].translate( v2(100, 350) );
		self.blocks[3].translate( v2(500, 350) );
		self.blocks[4].translate( v2(100, 600) );
		self.blocks[5].translate( v2(500, 600) );

	def set_config(self, config):
		if not isinstance(config, Config) and len(vec) != 2:
			raise Exception('Wrong Configuration class. Has to be a Config instance')
		self.robot.center = v2( config[0], config[1] );

	def get_config(self):
		'''get the configuration of the robot'''
		return Config( [self.robot.center.x, self.robot.center.y] );

	def render(self, surf, color_):
		''''render the robot to screen using pygame.'''
		for block in self.blocks:
			block.render(surf, (100, 100, 100));

		pos = self.get_config();
		pygame.draw.circle( surf, (200,0,0), ( int(pos[0]), int(pos[1]) ), int(self.robot.radius) );
		pass;

	def __robot2wall__( self):
		point = self.robot.center;
		return min([point.x, self.dimensions[0]-point.x, point.y, self.dimensions[1]-point.y])-self.robot.radius;

	def __robot2block__( self, mode='L2' ):
		dists = [];
		point = self.robot.center;
		for block in self.blocks:
			inside = 1.0;
			if block.contains(point):
				inside = -1.0;
			dists.append( block.distance2point(point, mode) * inside );
		return min(dists) - self.robot.radius;

	def is_valid_config(self, config):
		'''test if a robot is valid'''
		oldcfg = self.get_config();
		self.set_config(config);
		dist = min( [ self.__robot2block__(), self.__robot2wall__() ] );
		self.set_config(oldcfg);
		return dist > 0;

	def config_clearance( self, config, mode='L2' ):
		'''Get clearance of a given configuration'''
		oldcfg = self.get_config();
		self.set_config(config);
		dist = min( [ self.__robot2block__(mode), self.__robot2wall__() ] );
		self.set_config(oldcfg);
		return dist;