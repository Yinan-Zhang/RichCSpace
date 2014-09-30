import sys, os, pygame, math
import numpy

sys.path.append('../basics/math')

from geometry import v2, sphere2d
from hyper_geometry import *
from l1_geometry import *
#from hyper_triangle import *

code = 0; ## code for each triangle as a reference 

class Triangle:
	def __init__(self, sphere1, sphere2, sphere3):
		'''sphere1~3 are hyper_spheres '''
		self.vertices = [sphere1.center, sphere2.center, sphere3.center];
		self.spheres = [sphere1, sphere2, sphere3];
		self.valid_triangle = True;
		global code;
		self.code = code;
		code += 1;

	def __hash__( self ):
		return hash(self.code);

	def dist_edges(self):
		'''return distinguish edges. (1,2) and (2,1) edges are considered the same'''
		return [ (self.spheres[0], self.spheres[1]), (self.spheres[0], self.spheres[2]),(self.spheres[1], self.spheres[2]) ];

	def edges(self):
		return [(self.spheres[0],self.spheres[1]),(self.spheres[1],self.spheres[0]), (self.spheres[0],self.spheres[2]), (self.spheres[2],self.spheres[0]), (self.spheres[1],self.spheres[2]), (self.spheres[2],self.spheres[1]) ]

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

	def is_filled_l1(self):
		'''determin if filled in l1 metric'''
		if self.spheres[0].intersects(self.spheres[1]) and self.spheres[0].intersects(self.spheres[2]) and self.spheres[1].intersects(self.spheres[2]):
			return True;
		return False;	

	def is_filled(self):
		if isinstance(self.spheres[0], l1_sphere ):
			return self.is_filled_l1();

		A = self.spheres[0].center;
		B = self.spheres[1].center;
		C = self.spheres[2].center;

		l1 = (A-B).r();
		l2 = (A-C).r();
		l3 = (B-C).r();
		cos_a = (B-A).dot(C-A) / ( l1 * l2 );
		sin_a = math.sqrt( 1 - cos_a**2 );

		A = v2(0.0, 0.0);							r_a = self.spheres[0].radius;
		B = v2(l1, 0);								r_b = self.spheres[1].radius;
		C = v2(l2*cos_a, l2*sin_a);					r_c = self.spheres[2].radius;

		ball1 = sphere2d( A, self.spheres[0].radius );
		ball2 = sphere2d( B, self.spheres[1].radius );
		ball3 = sphere2d( C, self.spheres[2].radius );


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

		# Determine if the intersection is inside any spheres
		#for sphere in self.spheres:
		#	if sphere.contains( rad_center ):
		#		return True
		if ball1.contains(rad_center) or ball2.contains(rad_center) or ball3.contains(rad_center):
			return True;
		return False;



class Triangulator:
	def __init__(self, spheres):
		self.spheres = spheres;

	def triangulate(self):
		def __add2dict__(dct, key, content):
			'''Add a content to a dictionary. dct[key] should be an array'''
			if not dct.has_key(key):
				dct[key] = [content];
			elif not content in dct[key]:
				dct[key].append(content);

		def __add_edge_2_dict__(dct, edge_key, content):
			'''Add a content to a dictionary. dct[key] should be an array'''
			edge1 = (edge_key[0], edge_key[1]);
			edge2 = (edge_key[1], edge_key[0]);
			if dct.has_key(edge1) and dct.has_key(edge2):
				for elem in dct[edge2]:
					if not elem in dct[edge1]:
						dct[edge1].append(content);
				del dct[edge2];
			elif dct.has_key(edge1) and not dct.has_key(edge2) and not content in dct[edge1]:
				dct[edge1].append(content);
			elif dct.has_key(edge2) and not dct.has_key(edge1) and not content in dct[edge2]:
				dct[edge2].append(content);
			else:
				dct[edge1] = [content];

		#######################################
		####       Delaunay Triangulation
		from scipy.spatial import Delaunay
		points = [];
		for sphere in self.spheres:
			points.append(sphere.center.to_list());

		points_np = numpy.array(points);
		triangles_index = Delaunay(points_np);

		triangle_set = {};
		sphere_tri_dict = {};
		edge_tri_dict = {};

		#########################################
		#### 	    Building filled triangles
		####    And sphere-triangle edge-triangle dict
		for tri_idx in triangles_index.simplices:
			sphere0 = self.spheres[tri_idx[0]]
			sphere1 = self.spheres[tri_idx[1]]
			sphere2 = self.spheres[tri_idx[2]]
			triangle = Triangle(sphere0, sphere1, sphere2);
			if triangle.is_filled():
				triangle_set[triangle] = 1;
				__add2dict__(sphere_tri_dict, sphere0, triangle);
				__add2dict__(sphere_tri_dict, sphere1, triangle);
				__add2dict__(sphere_tri_dict, sphere2, triangle);
				__add_edge_2_dict__(edge_tri_dict, (sphere0, sphere1), triangle);
				__add_edge_2_dict__(edge_tri_dict, (sphere0, sphere2), triangle);
				__add_edge_2_dict__(edge_tri_dict, (sphere1, sphere2), triangle);

		return triangle_set, sphere_tri_dict, edge_tri_dict;

