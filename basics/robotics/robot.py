
__all__ = [
  'DiffDriveConfig', 'Robot', 'DiffDriveRobot'
]

'''
This file contains classes related to robots.
- DiffDriveConfig 	|	Differential drive configuration.
- Robot 			|	base class of robots.
- DiffDriveRobot	|	Differential Drive Robot.
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

import sys
sys.path.append('../math')

import pygame;
import math;

from geometry import *
from configuration import *

class DiffDriveConfig( Config ):
	'''Diff Drive configuration'''
	def __init__(self, *args):
		"""@param *args: list of arguments. """
		Config.__init__(*args);
		if len(*args) != 3:
			raise Exception('The dimension has to be 3: ( x, y, phi )')
		self.pos = v2(self.__getitem__(0), self.__getitem__(0));
		self.orient = orient;

	@property
	def x(self):
		return self.pos.x;

	@property
	def y(self):
		return self.pos.y;

class Robot:
	'Robot base class'
	def __init__(self):
		self.config = None;
		pass;

	#def position(self):
	#	'''returns the position of the robot.'''
	#	pass;

	def set_config(self, config):
		'''set configuration of the robot.
		@param config: Config 	robot configuration.'''
		self.config = config;

	def get_config(self):
		'''get the configuration of the robot'''
		return self.config;

	def render(self, surf, color_):
		''''render the robot to screen using pygame.'''
		pass;

	def intersects(self, polygon):
		'''test if the robot intersects with a polygon
		@param polygon: Polygon'''
		return False;

	def def is_valid_config(self, config):
		'''test if a robot is valid'''
		return True;


class DiffDriveRobot( Robot ):
	'''Differential Drive Robot class. A diff drive robot will be simplidied 
	as a line segment with wheels in two ends'''

	def __init__(self, length, config):
		'''@param length: the length of the robot
		@param config: DiffDriveConfig	|	diff drive configuration
		'''
		self.length = float(length);
		self.config = config;
		self.collision = False;

	def position(self):
		return self.config.pos;
		
	def orientation(self):
		return self.config.orient;

	pos = position;			# alias
	orient = orientation;	# alias

	def get_line(self):
		start = v2( self.config.pos.x - self.length/2.0*math.sin(self.config.orient),
				  self.config.pos.y + self.length/2.0*math.cos(self.config.orient));
		end   = v2( self.config.pos.x + self.length/2.0*math.sin(self.config.orient),
				  self.config.pos.y - self.length/2.0*math.cos(self.config.orient));

		return line_segment(start, end);

	def intersects(self, polygon):
		botline = self.get_line();
		self.collision = False;
		self.collision = polygon.inside( self.config.pos )
		if self.collision:
			return True;

		for line in polygon.lines:
			if line.intersects_segment(botline):
				self.collision = True;

		return self.collision;

	def set_config(self, config):
		'''Set robot to a config'''
		self.config = config;
		return self.get_line();

	def render( self, surf, color_=None ):
		'''Render the differential drive to the screen'''
		if self.collision == False:
			color = (80, 255, 80);
		else:
			color = (255,0,0);

		if color_ is not None:
			color = color_;

		line = self.get_line();
		line.render( surf, color, 5 );

		temp = v2( self.config.pos.x + self.length/5.0*math.cos(self.config.orient),
				  self.config.pos.y + self.length/5.0*math.sin(self.config.orient));
		pygame.draw.line( surf, color, (self.config.pos.x, self.config.pos.y), (temp.x, temp.y), 4 )

		return;

