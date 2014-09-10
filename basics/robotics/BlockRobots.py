
__all__ = [
  'BlockRobot', 'BlockRobotConfig'
]

'''
This file contains classes related to robots.
- BlockRobot
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

import sys, os, copy
sys.path.append('../math')

import pygame;
import math;

from geometry import *
from polygon import *
from hyper_geometry import *
from configuration import *
from robot import *

class BlockRobotConfig(Config):
	def __init__(self, x1, y1, x2, y2):
		Config.__init__( self, [x1, y1, x2, y2]);

class Block(Polygon):
	'''Block is a sub-class of polygon where all lines in a Block has normal direction parrelal either to x-axis or y-axis'''

	def __init__( self, pntlist ):
		Polygon.__init__(self, pntlist);
		self.x_lines = []	# lines with normal direction in x axis
		self.y_lines = []	# lines with normal direction in y axis
		for line in self.lines:
			mink = line.start - line.end;
			if mink.x == 0:
				self.x_lines.append(line);
			elif mink.y == 0:
				self.y_lines.append(line);

	def distance( self, other ):
		'''Distance to another block. returned as (x,y) tuple'''
		choices = []
		for vert in self.vertices:
			closest, dist = other.closest_point(vert);
			choices.append( closest - vert );
			#print closest-vert

		min_dist = 100000000;
		chosen = None;
		for choice in choices:
			if choice.r() < min_dist:
				min_dist = choice.r();
				chosen = choice;

		return chosen;

	def distance2wall(self, dimensions = (800,800)):
		'''distance to wall, return movement vector'''
		dists = []
		for vert in self.vertices:
			dists.append( min([ vert.x, vert.y, math.fabs(dimensions[0]-vert.x), math.fabs(dimensions[1]-vert.y) ]) )
		return min(dists);

class BlockRobot( Robot ):
	def __init__(self, unit_len=15):
		self.unit_size = unit_len;
		#pntlist = [ v2(0,0), v2(4,0), v2(4,-3), v2(3,-3), v2(3,-1), v2(1,-1), v2(1,-7), v2(4,-7), v2(4,-8), v2(0,-8) ];
		pntlist = [ v2( 0,0 ), v2( 4,0 ), v2( 4,-4 ), v2( 0, -4 ) ];
		for point in pntlist:
			point *= self.unit_size;

		block2pnts = copy.deepcopy( pntlist );

		#block2pnts = [ v2(0,0), v2(4,0), v2(4,-3), v2(3,-3), v2(3,-1), v2(1,-1), v2(1,-5), v2(4,-5), v2(4,-6), v2(0,-6) ];

		#for point in block2pnts:
		#	point *= self.unit_size;

		angle = math.pi;
		for point in block2pnts:
			point.x = point.x*math.cos(angle)-point.y*math.sin(angle);
			point.y = point.x*math.sin(angle)+point.y*math.cos(angle);

		block1 = Block( pntlist );
		block2 = Block( block2pnts );
		self.blocks = [block1, block2];
		self.config = BlockRobotConfig( 0,0, 0, 0 )

	def set_config(self, config):
		if not isinstance(config, BlockRobotConfig):
			config = BlockRobotConfig(config[0], config[1], config[2], config[3]);
			#raise Exception('Wrong Configuration class. Has to be a BlockRobotConfig instance')
		old_cfg = copy.copy(self.config);
		self.config = config;
		vect1 = v2( self.config[0]-old_cfg[0], self.config[1]-old_cfg[1]);
		vect2 = v2( self.config[2]-old_cfg[2], self.config[3]-old_cfg[3]);
		self.blocks[0].translate(vect1);
		self.blocks[1].translate(vect2);

	def get_config(self):
		return self.config;

	def is_valid_config(self, config):
		if not isinstance(config, BlockRobotConfig):
			config = BlockRobotConfig(config[0], config[1], config[2], config[3]);
		oldconfig = copy.copy(self.config);
		self.set_config( config );
		for i in range(0,2):
			for vert in self.blocks[i].vertices:
				if vert.x <=0 or vert.y <= 0 or vert.x >= 800 or vert.y >= 800:
					return False;

		intersects = self.blocks[0].intersects_poly( self.blocks[1] );
		self.set_config( oldconfig );
		return not intersects;

	def config_clearance( self, config, mode='L2' ):
		'''get the clearance of a given configuration without changing current config.
		@param mode: str 'L1' or 'L2' distance '''  
		if self.is_valid_config(config):
			collision_cfg = self.get_collission_config(config);
			if mode == 'L2' or mode == 'l2':
				return min( [self.clearance2wall(config), (collision_cfg-config).r()  * 1.41421356237]);
			elif mode == 'L1' or mode == 'l1':
				return min( [self.clearance2wall(config), (collision_cfg-config).l1()] );
		else:
			return -1.0;

	def clearance2wall(self, config):
		'''given a configuration, return its clearance to wall'''
		old_cfg = copy.copy(self.config);
		self.set_config(config);
		dists = []
		dists.append( self.blocks[0].distance2wall());
		dists.append( self.blocks[1].distance2wall());
		self.set_config(old_cfg);
		return min(dists);

	def get_collission_config( self, config ):
		'''given a configuration, get the nearest collission config'''
		if not isinstance(config, BlockRobotConfig):
			config = BlockRobotConfig(config[0], config[1], config[2], config[3]);
		old_cfg = copy.copy(self.config);
		self.set_config(config);
		dist_vec = self.blocks[0].distance(self.blocks[1]);
		collision_cfg = BlockRobotConfig( config[0]+dist_vec.x/2.0, config[1]+dist_vec.y/2.0, config[2]-dist_vec.x/2.0, config[3]-dist_vec.y/2.0 );
		self.set_config(old_cfg);
		return collision_cfg;

	def render(self, surf, alpha):
		s = pygame.Surface( surf.get_size() )
		s.set_alpha(alpha)
		s.fill((255,255,255))
		
		self.blocks[0].render(s, ( 26, 152, 80, alpha ));
		self.blocks[1].render(s, ( 230, 97, 1, alpha ));

		surf.blit(s, (0,0));
		pygame.display.update();

'''
if __name__ == '__main__':
	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	robot = BlockRobot( );
	startConfig = BlockRobotConfig(100,200, 700, 600);
	goalConfig = BlockRobotConfig(400,400, 482.5, 332.5);
	testConfig = BlockRobotConfig(311,667,725,427);

	collision_cfg = robot.get_collission_config(testConfig);

	robot.set_config( testConfig );
	robot.render(DISPLAYSURF, 250);
	pygame.display.update();

	robot.set_config( collision_cfg );
	robot.render(DISPLAYSURF, 200);
	pygame.display.update();

	pygame.image.save(DISPLAYSURF, 'BlockRobot.PNG');
'''
