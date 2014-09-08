

__all__ = [
  'Polygon'
]

'''
This file contains classes related to polygons in a plane.
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

import sys, os, math
import pygame

from geometry import *


class Polygon:
	"""Polygon class. An obstacle is defined as a polygon."""
	def __init__( self, ptlist ):
		"""@param ptlist: v2[] 	Points list or v2() list, anti-clockwise ordered."""
		self.vertices = ptlist;
		self.lines = [];
		for i in range(1, len(ptlist)):
			line  = line_segment(ptlist[i-1], ptlist[i]);
			self.lines.append(line);

		start = ptlist[-1];
		end   = ptlist[0];
		self.lines.append( line_segment( start, end ) );
		pass;

	def render(self, surface, color):
		"""render the polygon to surface."""
		pointlist = [];
		for vertex in self.vertices:
			pointlist.append( (int(vertex.x), int(vertex.y)) );
		pygame.draw.polygon(surface, color, pointlist);
		pass;

	def translate( self, vect ):
		'''translate the polygon along a vect '''
		self.lines = [];
		self.vertices[0] += vect;
		for i in range(1, len(self.vertices)):
			self.vertices[i] += vect;
			line  = line_segment(self.vertices[i-1], self.vertices[i]);
			self.lines.append(line);

		start = self.vertices[-1];
		end   = self.vertices[0];
		self.lines.append( line_segment( start, end ) );
		pass;

	def intersects(self, line_seg):
		"""polygon-line intersectiong test.
		@param line_seg: line_segment."""
		for line in self.lines:
			if line.intersects_segment( line_seg ):
				return True;
		return False;

	def intersects_poly(self, other):
		'''determine if self intersects another polygon'''
		for line in other.lines:
			if self.intersects( line ):
				return True;
		return False;

	def dist2line(self, line_seg):
		'''returns the distance to a line segment.
		@param line_seg: line_segment'''
		dists = []
		for line in self.lines:
			dists.append(line.dist_line_seg(line_seg));
		return min(dists);

	def contains( self, point ):
		'''Assume the polygon is a simple polygon. determine if point is inside the polygon.
		@param point: v2	Point.'''
		ray = line_segment( point, v2( 3000, 3000 ) );
		intersectTimes = 0;
		for line in self.lines:
			if line.intersects_segment( ray ):
				intersectTimes += 1;

		if intersectTimes % 2 == 1:
			return True;
		else:
			return False;

	def closest_point(self, point):
		'''get the nearest point in the polygon to a point'''
		nearestPoint = None;
		minDist = 10000000000.0;
		for line in self.lines:
			temp = line.closest_point( point );
			dist = math.sqrt( (point.x-temp.x)**2 + (point.y-temp.y)**2);
			if dist < minDist:
				nearestPoint = temp;
				minDist = dist;
		return nearestPoint, minDist;