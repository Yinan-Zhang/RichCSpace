import sys, os, pygame, math
import numpy

sys.path.append('../basics/math')

from geometry import v2
from hyper_geometry import *
from hyper_triangle import *

class Triangle:
	def __init__(self, sphere1, sphere2, sphere3):
		'''sphere1~3 are hyper_spheres '''
		self.vertices = [sphere1.center, sphere2.center, sphere3.center];
		self.spheres = [sphere1, sphere2, sphere3];
		self.valid_triangle = True;

	def valid_edges(self):
		'''if an edge is between two intersecting spheres, it's a valid edge'''
		edges = [];
		if self.spheres[0].intersects( self.spheres[1] ):
			edges.append( (self.spheres[0], self.spheres[1]) );
		if self.spheres[0].intersects( self.spheres[2] ):
			edges.append( (self.spheres[0], self.spheres[2]) );
		if self.spheres[1].intersects( self.spheres[2] ):
			edges.append( (self.spheres[1], self.spheres[2]) );

		if len(edges) < 3:
			self.valid_triangle = False;

		return edges;

	def is_filled(self, surf):
		A = self.spheres[0].center;
		B = self.spheres[1].center;
		C = self.spheres[2].center;

		l1 = (A-B).r();
		l2 = (A-C).r();
		l3 = (B-C).r();
		cos_a = (B-A).dot(C-A) / ( l1 * l2 );
		sin_a = math.sqrt( 1 - cos_a**2 );

		A = v2(0.0, 0.0);							r_a = ball1.radius;
		B = v2(l1, 0);								r_b = ball2.radius;
		C = v2(l2*cos_a, l2*sin_a);					r_c = ball3.radius;

		ball1 = sphere( A, self.spheres[0].radius );
		ball2 = sphere( B, self.spheres[1].radius );
		ball3 = sphere( C, self.spheres[2].radius );

		# 1. First Radical Axis
		mid1 = A + (B-A).normalize() * ( l1**2 + r_a**2 - r_b**2 ) / (2 * l1); 
		if ball3.contains(mid1):
			return True;
		k1 = 0.0;
		if (A-B).y == 0:
			k1 = 100000000000.0;
		elif (A-B).x == 0:
			k1 = 0.0;
		else:
			k1 = -1.0 / ( (B.y-A.y)/(B.x-A.x) );

		# 2.1 Second Radical Axis
		mid2 = A + (C-A).normalize() * ( l2**2 + r_a**2 - r_c**2 ) / (2 * l2);
		if ball2.contains( mid2 ):
			return True;
		k2 = 0.0;
		if (A-C).y == 0:
			k2 = 1000000000000.0;
		elif (A-C).x == 0:
			k2 = 0.0;
		else:
			k2 = -1.0 / ( (A.y-C.y)/(A.x-C.x) );

		# 2.2 Third Radical Axis
		mid3 = B + (C-B).normalize() * ( l3**2 + r_c**2 - r_c**2 ) / (2 * l3); 
		if ball1.contains(mid3):
			return True;

		# 3. Radical center is the intersection of two axises
		inter_x = (k1*mid1.x - k2*mid2.x + mid2.y - mid1.y) / (k1-k2);
		inter_y = k1*( inter_x - mid1.x ) + mid1.y;
		rad_center = v2( inter_x, inter_y );

		pygame.draw.circle( surf, (255,0,255), (int(rad_center.x), int(rad_center.y)), 3 )

		# Determine if the intersection is inside any spheres
		for sphere in self.spheres:
			if sphere.contains( rad_center ):
				return True

		return False;