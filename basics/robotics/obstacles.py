

__all__ = [
  'ObstManager'
]

'''
This file contains classes related to the management of obstacles.
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

import sys
sys.path.append('../math')

from robot import *
from geometry import *

class ObstManager:
	'''Obstacle manager that controls all the obstacles in the space'''
	def __init__(self, obstacles):
		'''@param obstacles: Polygon[]	|	a list of obstacles'''
		self.obsts = obstacles;

	def intersects(self, robot):
		'''determine if the robot intersects with any obstacles in the space'''
		if robot is None:
			return False;
		if self.inside( robot.position() ):
			return True;
		for obst in self.obsts:
			if( robot.intersects(obst) ):
				return True;
		return False;

	def dist2obsts(self, robot):
		'''return the min dist from the robot to any obstacles.'''
		if not isinstance(robot, DiffDriveRobot):
			raise Exception( 'The robot must be a diff drive robot' )
		dists = [];
		robot_line = robot.get_line();
		for obst in self.obsts:
			dists.append( obst.dist2line(robot_line) );
		return min(dists);

	def time2obsts(self, robot):
		'''return the min time for a robot to collide with any obstacles'''
		dist = self.dist2obsts(robot);
		return dist / 5.0;

	def closest_point(self, point):
		'''get the nearest point in obstacles to a point. 
		!!!This works only in 2d c-space!!!'''
		minDist = 10000000000;
		nearest = None;
		for obst in self.obsts:
			near, dist = obst.closest_point(point);
			if dist < minDist:
				nearest = near;
				minDist = dist;

		inside = 1;
		if self.inside(point):
			inside = -1;
		return nearest, minDist*inside;

	def inside( self, pnt ):
		'''test if a point is inside any polygon.
		!!!This works only in 2d c-space!!!'''
		for obst in self.obsts:
			if obst.contains(pnt):
				return True;
		return False;

	def render(self, surf):
		for obst in self.obsts:
			obst.render( surf, (60,60,60) );
		