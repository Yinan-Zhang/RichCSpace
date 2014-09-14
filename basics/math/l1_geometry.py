
import sys, os, math

from hyper_geometry import *


class l1_sphere:
	def __init__( self, center, radius ):
		''' Open high dimensional sphere
		@param center: (vec) the center of the sphere
		@param radius: (number) the radius of the sphere'''
		if isinstance(center, list):
			center = vec(center);
		self.center = center;
		self.radius = radius;

	def contains( self, point ):
		'''determine if the point is inside the sphere
		@param point: (vec) the point'''
		dist = (point - self.center).l1();
		return dist < self.radius;

	def intersects( self, other ):
		'''determine if the other sphere is intersecting with self'''
		center_dist = (self.center - other.center).l1();
		return center_dist < self.radius + other.radius;