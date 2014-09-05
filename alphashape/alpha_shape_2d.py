import sys, os, pygame, math
import numpy

from scipy.spatial import Delaunay

sys.path.append('../basics/math')

from geometry import *


class Triangle:
	def __init__(self, sphere1, sphere2, sphere3):
		'''v1, v2, v3 are all instances of geometry.v2(x,y)'''
		self.vertices = [sphere1.center, sphere2.center, sphere3.center];
		self.spheres = [sphere1, sphere2, sphere3];
		self.valid_triangle = True;

	def valid_edges(self):
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
		ball1 = self.spheres[0];
		ball2 = self.spheres[1];
		ball3 = self.spheres[2];
		A = v2(ball1.center.x, ball1.center.y);		r_a = ball1.radius;
		B = v2(ball2.center.x, ball2.center.y);		r_b = ball2.radius;
		C = v2(ball3.center.x, ball3.center.y);		r_c = ball3.radius;

		# 1. First Radical Axis
		l1 = (A-B).r();
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
		l2 = (A-C).r();
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
		l3 = (B-C).r();
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

	def render(self, surface,  color = ( 0, 255, 0 ) ):
		pointlist = [ (self.vertices[0].x, self.vertices[0].y), (self.vertices[1].x, self.vertices[1].y), (self.vertices[2].x, self.vertices[2].y) ];
		mode = not self.is_filled(surface);
		pygame.draw.polygon( surface, color, pointlist, mode );

class AlphaShape2D:
	def __init__( self ):
		self.spheres = [];

	def triangulate(self, spheres):
		'''@param spheres: geometry.sphere '''
		pnt_array = [];
		for sphere in spheres:
			pnt_array.append( (sphere.center.x, sphere.center.y) );

		np_points = numpy.array( pnt_array );
		tris 	  = Delaunay( np_points );
		triIdx    = tris.vertices;
		triangles = [];
		for tri in triIdx:
			sphere1 = spheres[ tri[0] ];
			sphere2 = spheres[ tri[1] ];
			sphere3 = spheres[ tri[2] ];
			triangles.append( Triangle(sphere1, sphere2, sphere3) );

		return triangles;

	def build_power_diagram( self, spheres, surf, width, height ):
		for x in range(0, width):
			for y in range(0, height):
				power_dists = [];
				pnt = v2(x, y);
				for sphere in spheres:
					power_dists.append( (pnt-sphere.center).r()**2 - sphere.radius**2 );
				min_dist = min(power_dists);
				power_dists.remove(min_dist);
				min_dist2 = min(power_dists);
				if math.fabs(min_dist - min_dist2) <= 50.0:
					pygame.draw.circle( surf, (255,0,255), (x,y), 1 );

	def build_alpha_shape(self, spheres, surf=None):
		triangles = self.triangulate(spheres);
		edges = []
		valid_triangles = [];


		for tri in triangles:
			valid_edges = tri.valid_edges();
			for edge in valid_edges:
				edges.append( edge );
			if tri.valid_triangle:
				valid_triangles.append( tri );

		if surf:
			for tri in valid_triangles:
				tri.render(surf);
			for edge in edges:
				end1 = (int(edge[0].center.x), int(edge[0].center.y) );
				end2 = (int(edge[1].center.x), int(edge[1].center.y) );
				pygame.draw.line( surf, ( 0,250,0 ), end1, end2, 2 );

def load_data( filename):
	'''load spheres information from file'''
	file2read = open( filename, 'r' );
	lineNum = 0;
	spheres = [];
	for line in file2read:
		lineNum += 1;
		if lineNum > 43:
			break;
		strSphere = line;
		info = strSphere.split( '\t' );
		pos = [0] * 2;
		pos[0] = float( info[0] );
		pos[1] = float( info[1] );
		radius = float( info[2] );
		spheres.append( sphere(v2(pos[0], pos[1]), radius) );
	return spheres;

def test():
	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	spheres = load_data('balls.txt');
	for sphere in spheres:
		pygame.draw.circle( DISPLAYSURF, (250,0,0), (int(sphere.center.x),int(sphere.center.y)), int(sphere.radius), 1 );

	alpha = AlphaShape2D();
	alpha.build_alpha_shape(spheres, DISPLAYSURF);
	#alpha.build_power_diagram(spheres, DISPLAYSURF, WIDTH, HEIGHT);

	pygame.image.save( DISPLAYSURF, 'test.PNG' );

if __name__ == "__main__":
	test()



