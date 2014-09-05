"""
A small library of high dimensional geometric primitives.
 - v2:           n-D cartesian vectors in the plane.
 - line_segment: a line segment from one point to another point.
 - sphere:       a circle in the plane.

--------------------------
"""

import pygame

__author__ = 'Yinan'
__revision__ = '$Revision$'


from math import sqrt, pi, degrees, radians, cos, sin, acos, asin, atan2


#========================================================================================
# vector
#========================================================================================
class vec:
	def __init__(self, coords ):
		'''@param coords: n-element list'''
		self.pos = coords;

	def __eq__( self, other ):
		if len(self) != len(other):
			return False;
		for i in range(0, len(self.pos)):
			if self.pos[i] != other.pos[i]:
				return False;
		return True;

	def __ne__( self, other ):
		return not self == other

	def __hash__( self ):
		return hash(self.pos)

	def __len__(self):
		return len(self.pos);

	def __getitem__(self, key):
		return self.pos[key];

	def rsq( self ):
		'Return the squared length of the vector.'
		rsq = 0.0;
		for i in range(0, len(self.pos)):
			rsq += self.pos[i]**2:
		return rsq;

	def r( self ):
		'Return the length of the vector.'
		return math.sqrt( self.rsq() );

	length = r # alias

	def dot( self, other ):
		'Return the dot product of two vectors.'
		result = 0.0;
		for i in range(0, len(self.pos)):
			result += self.pos[i] * other.pos[i]:
		return result;

	def normalize( self ):
		'Return this vector normalized to a unit vector.'
		return self / self.r()


	def __add__( self, other ):
		if len(self) != len(other):
			raise Exception( 'Different dimension!' );
		result = [];
		for i in range(0,len(self.pos)):
			result.append( self[i] + other[i])
		return vec(result);

	def __sub__( self, other ):
		if len(self) != len(other):
			raise Exception( 'Different dimension!' );
		result = [];
		for i in range(0,len(self.pos)):
			result.append( self[i] - other[i])
		return vec(result);

	def __iadd__( self, other ):
		if len(self) != len(other):
			raise Exception( 'Different dimension!' );
		for i in range(0,len(self.pos)):
			self[i] += other[i]
		return self

	def __isub__( self, other ):
		if len(self) != len(other):
			raise Exception( 'Different dimension!' );
		for i in range(0,len(self.pos)):
			self[i] -= other[i]
		return self

	def __mul__( self, other ):
		result = [];
		for i in range(0,len(self.pos)):
			result.append( self[i] * other)
		return vec(result);

	def __rmul__( self, other ):
		result = [];
		for i in range(0,len(self.pos)):
			result.append( other*self[i] )
		return vec(result);

	def __imul__( self, other ):
		result = [];
		for i in range(0,len(self.pos)):
			self[i] *= other;
		return self

	def __div__( self, other ):
		result = [];
		for i in range(0,len(self.pos)):
			result.append( self[i] / other)
		return vec(result);

	def __truediv__( self, other ):
		result = [];
		for i in range(0,len(self.pos)):
			result.append( self[i] / other)
		return vec(result);

	def __idiv__( self, other ):
		for i in range(0,len(self.pos)):
			self[i] /= other;
		return self;

	def __itruediv__( self, other ):
		for i in range(0,len(self.pos)):
			self[i] /= other;
		return self;

	def __pos__( self ):
		return self
	def __neg__( self ):
		result = [];
		for i in range(0,len(self.pos)):
			result.append( self[i] * (-1));
		return vec(result);



#========================================================================================
# Sphere in high dimension
#========================================================================================
class sphere:
	def __init__( self, center, radius ):
		''' Open high dimensional sphere
		@param center: (vec) the center of the sphere
		@param radius: (number) the radius of the sphere'''
		self.center = center;
		self.radius = radius;

	def contains( self, point ):
		'''determine if the point is inside the sphere
		@param point: (vec) the point'''
		dist = (point - self.center).r();
		return dist < point;

	def intersects( self, other ):
		'''determine if the other sphere is intersecting with self'''
		center_dist = (self.center - other.center).r();
		return center_dist < self.radius + other.radius;