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

class WarehouseRobot2( Robot ):
	def __init__(self, dimensions):
		'''@param dimensions: world dimensions.'''
		self.dimensions = dimensions;
		points = [ v2(0,0), v2(200,0), v2(200,100), v2(0,100) ];
		self.blocks = [];
		self.robots = [ sphere2d(v2(0.0,0.0), 15.0), sphere2d(v2(800.0,800.0), 15.0) ];
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
		if not isinstance(config, Config) and len(vec) != 4:
			raise Exception('Wrong Configuration class. Has to be a Config instance')
		self.robots[0].center = v2( config[0], config[1] );
		self.robots[1].center = v2( config[2], config[3] );

	def get_config(self):
		'''get the configuration of the robot'''
		return Config( [self.robots[0].center.x, self.robots[0].center.y, self.robots[1].center.x, self.robots[1].center.y] );

	def render(self, surf, color_):
		''''render the robot to screen using pygame.'''
		for block in self.blocks:
			block.render(surf, (100, 100, 100));

		pos = self.get_config();
		pygame.draw.circle( surf, (200,0,0), ( int(pos[0]), int(pos[1]) ), int(self.robots[0].radius) );
		pygame.draw.circle( surf, (200,0,0), ( int(pos[2]), int(pos[3]) ), int(self.robots[1].radius) );
		pass;

	def __robot2robot__(self, mode = 'L2'):
		if mode == 'L2' or mode == 'l2':
			dist = (self.robots[0].center - self.robots[1].center).r() - ( self.robots[0].radius + self.robots[1].radius );
		elif: mode == 'L1' or mode == 'l1':
			dist = (self.robots[0].center - self.robots[1].center).l1() - ( self.robots[0].radius + self.robots[1].radius );
		return dist/2.0;

	def __robot2wall__( self):
		point1 = self.robot[0].center;
		point2 = self.robot[1].center;
		dist1 = min([point1.x, self.dimensions[0]-point1.x, point1.y, self.dimensions[1]-point1.y])-self.robot[0].radius;
		dist2 = min([point2.x, self.dimensions[2]-point2.x, point2.y, self.dimensions[3]-point2.y])-self.robot[1].radius;
		return min( [dist1, dist2] );

	def __robot2block__( self, mode='L2' ):
		dists = [];
		point1 = self.robots[0].center;
		for block in self.blocks:
			inside = 1.0;
			if block.contains(point1):
				inside = -1.0;
			dists.append( block.distance2point(point1, mode) * inside );

		point2 = self.robots[1].center;
		for block in self.blocks:
			inside = 1.0;
			if block.contains(point2):
				inside = -1.0;
			dists.append( block.distance2point(point2, mode) * inside );
			
		return min(dists) - self.robots[0].radius;

	def is_valid_config(self, config):
		'''test if a robot is valid'''
		oldcfg = self.get_config();
		self.set_config(config);
		dist = min( [ self.__robot2block__(), self.__robot2wall__(), self.__robot2robot__() ] );
		self.set_config(oldcfg);
		return dist > 0;

	def config_clearance( self, config, mode='L2' ):
		'''Get clearance of a given configuration'''
		oldcfg = self.get_config();
		self.set_config(config);
		dist = min( [ self.__robot2block__(mode), self.__robot2wall__(), self.__robot2robot__(mode) ] );
		self.set_config(oldcfg);
		return dist;