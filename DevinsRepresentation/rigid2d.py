
__all__ = [
  'Rigid2D'
]

'''
The file contains only one class:

Rigid2D:	
	A rigid body robot in a plan can be simplified as a rectangle.
	Using Devin's representation, the rectangle can be represented 
	using two points in the robot. ( Assume Width&Length are defined )
	|---o---|	A( x_a, y_a ) Mid point of the head.
	|       |   
	|       |
	|       |
	|       |   
	|---o---|	B( x_b, y_b ) Mid point of the tail.

	A state can be stated as a 4-element tuple ( x_a, y_a, x_b, y_b ).

	Robot displacement distance is the max distance of a corresponding 
	point. More formally:
	Let p be a point in robot R with state s, p' be the corresponding 
	point of R with state s'.
	displacement-distance( s,s' ) = max( |p-p'| ), for all points in R.

	Collision distance is the minimum distance between two objects.
'''

__author__ = 'Yinan Zhang	Dartmouth College'
__revision__ = '$Revision$'

import sys, random, copy, pdb
sys.path.append('../basics/math')

import pygame;
import math;

from geometry 	import *
from polygon 	import *

ROBOT_LENGTH = 40;
ROBOT_WIDTH  = 20;

class Rigid2D:
	def __init__(self, state, width = ROBOT_WIDTH, length = ROBOT_LENGTH):
		'''@param state: a 4-element vector. vec( x_a, y_a, x_b, y_b ).
		@param width: the width of the simplified rigid body robot in the plane.
		@param length: the length of the robot'''
		self.state = state;
		self.width = width;
		self.length= length;
		pass;

	def get_points(self):
		'''Get points of four corners.
			p1	|--| p2
				|  |
			p4	|--| p3

		'''
		A = v2(self.state[0], self.state[1]);
		B = v2(self.state[2], self.state[3]);
		hw = self.width/2.0;
		cos_alpha = (A.x-B.x)/(A-B).r();
		sin_alpha = (A.y-B.y)/(A-B).r();
		p1 = v2( A.x-hw*sin_alpha, A.y+hw*cos_alpha);
		p2 = v2( A.x+hw*sin_alpha, A.y-hw*cos_alpha);
		p3 = v2( B.x+hw*sin_alpha, B.y-hw*cos_alpha);
		p4 = v2( B.x-hw*sin_alpha, B.y+hw*cos_alpha);
		ptlist = [p1, p2, p3, p4];
		return ptlist;

	def __get_rectangle__( self ):
		'''get the rectangle shape of the robot.'''
		ptlist = self.get_points();
		return Polygon(ptlist);

	def render_head( self, surf ):
		A = v2(self.state[0], self.state[1]);
		pygame.draw.circle( surf, (250, 0,0), (int(A.x), int(A.y)), 5 );

	def render(self, surf, color, width = 0):
		'''render it to the screen'''
		rectangle = self.__get_rectangle__();
		rectangle.render(surf, color, width);
		A = v2(self.state[0], self.state[1]);
		pygame.draw.circle( surf, (250, 0,0), (int(A.x), int(A.y)), 5 );

	def set_state(self, state):
		if(self.is_state_valid(state)):
			self.state = state;
		pass;

	def displacement_dist(self, state):
		'''get the displacement distance between current state and given state'''
		old_state = copy.copy(self.state);
		origin_rect = self.__get_rectangle__();
		self.set_state(state);
		new_rect = self.__get_rectangle__();
		self.set_state(old_state);
		return origin_rect.displacement_dist(new_rect);

	def get_param_state(self):
		'''Get the parameterized state representation. In such representation, 
		the state of a rigid body in 2D is in SE(2) space. (x, y, theta)'''
		A = v2(self.state[0], self.state[1]);
		B = v2(self.state[2], self.state[3]);
		theta = math.atan2(A.y-B.y, A.x-B.x);
		mid = (A+B)/2.0;
		return (mid.x, mid.y, theta);

	def is_state_valid(self, state):
		A = v2(self.state[0], self.state[1]);
		B = v2(self.state[2], self.state[3]);
		return math.fabs( (A-B).r() - self.length ) <= 0.01;

	def get_classified_random_states( self, n, disp_dist ):
		'''A sphere in C-space for the rigid body is like this:
			V1	 ^
				 |
			 ....|....
			 .	 |   .
		-----.---o---.----------> V2
			 .   |O  .
			 ....|....
				 |
		Where V1 and V2 are two vertices of the rectangle. ( the whole sphere is in 4d space. )

		We want to map configs in the surface of the sphere back to our C-space. 
		'''

		sphere_samples = [];
		for i in range(n):
			sphere_samples.append( self.get_random_state(disp_dist) );

		origin_state = copy.copy(self.state);
		origin_pnts = self.get_points();
		P1_group = [];
		P2_group = [];
		P3_group = [];
		P4_group = [];

		for new_state in sphere_samples:
			self.set_state(new_state);
			new_pnts = self.get_points();
			# Find the point that is max dist
			max_idx = 0;
			max_dist = 0;
			for i in range(4):
				dist = (origin_pnts[i] - new_pnts[i]).r();
				if dist > max_dist:
					max_dist = dist;
					max_idx = i;
			if max_idx == 0:
				P1_group.append(new_state);
			elif max_idx == 1:
				P2_group.append(new_state);
			elif max_idx == 2:
				P3_group.append(new_state);
			elif max_idx == 3:
				P4_group.append(new_state);

		self.set_state(origin_state);
		print "Got {0} samples in p1 group.".format(len(P1_group));
		print "Got {0} samples in p2 group.".format(len(P2_group));
		print "Got {0} samples in p3 group.".format(len(P3_group));
		print "Got {0} samples in p4 group.".format(len(P4_group));
		return P1_group, P2_group, P3_group, P4_group;

	def __sphere__right__( self ):
		B = v2(self.state[2], self.state[3]);

	def get_random_state(self, disp_dist, surf = None):
		'''get a random state that has a fixed displacement-distance to current state.
		The idea is to have a random state first. Then pull/push the robot until the 
		displacement-distance is equal to disp_dist'''
		center  = v2( (self.state[0]+self.state[2])/2.0, (self.state[1]+self.state[3])/2.0)
		B_ 		= v2( random.randint(center.x-500, center.x+500), random.randint(center.y-500, center.y+500) );		# random point position
		theta 	= (random.randint(0, 360) / 360.0) * 2 * math.pi;		# random orientation.
		l 		= self.length;
		A_ 		= v2( B_.x + l * math.cos(theta), B_.y + l * math.sin(theta) );
		old_state = copy.copy(self.state);
		old_pnts  = self.get_points();

		new_state = (A_.x, A_.y, B_.x, B_.y);
		self.set_state(new_state);
		new_pnts  = self.get_points();
		self.set_state(old_state);

		# Find the point that is max dist
		#pdb.set_trace()
		max_idx = 0;
		max_dist = 0;
		for i in range(4):
			dist = (old_pnts[i] - new_pnts[i]).r();
			#print "\t" + str(dist)
			if dist > max_dist:
				max_dist = dist;
				max_idx = i;
		#print max_idx

		# Get max dist direction.
		max_dist_dir   = (new_pnts[max_idx] - old_pnts[max_idx])
		max_dist_dir_n = max_dist_dir.normalize();
		B_ = B_ - max_dist_dir + disp_dist * max_dist_dir_n;
		A_ = v2( B_.x + l * math.cos(theta), B_.y + l * math.sin(theta) );

		return (A_.x, A_.y, B_.x, B_.y)