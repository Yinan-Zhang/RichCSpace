
__all__ = [
  'Block Robot'
]

'''
This file contains classes related to robots.
- DiffDriveConfig 	|	Differential drive configuration.
- Robot 			|	base class of robots.
- DiffDriveRobot	|	Differential Drive Robot.
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
		for line1 in self.x_lines:
			for line2 in other.x_lines:
				x_dist = line1.start.x - line2.start.x;
				y_dist = min([line1.start.y-line2.start.y, line1.start.y-line2.end.y, line1.end.y-line2.start.y, line1.end.y-line2.end.y]);
				if y_dist <= 0:
					y_dist = 0;
				choices.append( v2(x_dist, y_dist) );

		for line1 in self.y_lines:
			for line2 in other.y_lines:
				y_dist = line1.start.y - line2.start.y;
				x_dist = min([line1.start.x-line2.start.x, line1.start.x-line2.end.x, line1.end.x-line2.start.x, line1.end.x-line2.end.x]);
				if x_dist <= 0:
					x_dist = 0;
				choices.append( v2(x_dist, y_dist) );

		min_dist = 10000000;
		chosen = None;
		for choice in choices:
			print choice 
			if choice.r() <= min_dist:
				min_dist = choice.r();
				chosen = choice;

		return chosen;


class BlockRobot( Robot ):
	def __init__(self, unit_len=15):
		self.unit_size = unit_len;
		pntlist = [ v2(0,0), v2(4,0), v2(4,-3), v2(3,-3), v2(3,-1), v2(1,-1), v2(1,-7), v2(4,-7), v2(4,-8), v2(0,-8) ];

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

		block1 = Polygon( pntlist );
		block2 = Polygon( block2pnts );
		self.blocks = [block1, block2];
		self.config = BlockRobotConfig( 0,0, 0, 0)

	def set_config(self, config):
		if not isinstance(config, BlockRobotConfig):
			raise Exception('Wrong Configuration class. Has to be a BlockRobotConfig instance')
		self.config = config;
		vect1 = v2( self.config[0], self.config[1]);
		vect2 = v2( self.config[2], self.config[3]);
		self.blocks[0].translate(vect1);
		self.blocks[1].translate(vect2);

	def get_config(self):
		return self.config;

	def is_valid_config(self, config):
		oldconfig = copy.copy(self.config);
		self.set_config( config );
		intersects = self.blocks[0].intersects( self.blocks[1] );
		self.set_config( oldconfig );
		return not intersects;


	def render(self, surf, alpha):
		s = pygame.Surface( surf.get_size() )
		s.set_alpha(alpha)
		s.fill((255,255,255))
		
		self.blocks[0].render(s, ( 26, 152, 80, alpha ));
		self.blocks[1].render(s, ( 230, 97, 1, alpha ));

		surf.blit(s, (0,0));
		pygame.display.update();

if __name__ == '__main__':
	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	#robot = BlockRobot( );
	#startConfig = BlockRobotConfig(100,200, 700, 600);
	#goalConfig = BlockRobotConfig(400,400, 482.5, 332.5);

	#robot.set_config( startConfig );
	#robot.render(DISPLAYSURF, 100);
	#pygame.display.update();

	#robot.set_config( goalConfig );
	#robot.render(DISPLAYSURF, 250);
	#pygame.display.update();

	block1 = Block([v2(100,100,), v2(120,100), v2(120,120), v2(100,120)]);
	block2 = Block([v2(130,130,), v2(150,130), v2(150,150), v2(130,150)]);
	block1.render(DISPLAYSURF, (26, 152, 80));
	block2.render(DISPLAYSURF, (230, 97, 1));

	print block1.distance(block2);

	pygame.image.save(DISPLAYSURF, 'BlockRobot.PNG');
