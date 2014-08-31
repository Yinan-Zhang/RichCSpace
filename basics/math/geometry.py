#! /usr/bin/python

"""
Reference: Trac 0.10.4 https://trac.assembla.com/icfpc08-csail/
"""

"""
A small library of 2D geometric primitives.
 - angle: a routine which normalizes angles to (-pi,pi].
 - v2:           2D cartesian vectors in the plane.
 - line_segment: a line segment from one 2D point to another 2D point.
 - circle:       a circle in the plane.
 - arc:          a directed arc of a circle.
 - path:         a list of line_segment and arc objects.

--------------------------
Modified by Yinan Zhang.
"""

import pygame

__author__ = 'Chris Lesniewski <ctl mit edu>'
__revision__ = '$Revision$'


from math import sqrt, pi, degrees, radians, cos, sin, acos, asin, atan2

__all__ = [
  'pi', 'degrees', # re-exported from math
  'angle', 'v2', 'v3', 'line_segment', 'circle', 'sphere', 'path',
]
 


# Evaluate this as a string so that constants can be folded.
exec '''
def angle( theta ):
  'Normalize an angle to the range [-pi,pi].'
  return ( ( theta + %(pi)r ) %% (2*%(pi)r) ) - %(pi)r
''' % { 'pi': pi }

#========================================================================================
# 2D vector
#========================================================================================
class v2( object ):
  'Represents a 2D point with coordinates (x,y).'
  __slots__ = ['x','y']

  def __init__( self, x, y ):
    self.x = x
    self.y = y

  @classmethod
  def polar( cls, r, radians ):
    'Construct a vector from a length and angle.'
    return cls( r*cos(radians), r*sin(radians) )

  @classmethod
  def from_angle( cls, radians ):
    'Construct a unit vector from an angle.'
    return cls( cos(radians), sin(radians) )

  def __str__( self ):
    return '(%.3f,%.3f)' % ( self.x, self.y )
  def __repr__( self ):
    return 'v2(%r,%r)' % ( self.x, self.y )
  def jgraph( self ):
    'Render as a jgraph command.'
    return 'newcurve pts %f %f marktype box\n' % ( self.x, self.y )


  def __eq__( self, other ):
    return self.x == other.x and self.y == other.y
  def __ne__( self, other ):
    return self.x != other.x or  self.y != other.y
  def __hash__( self ):
    return hash(( self.x, self.y ))

  def __len__(self):
    return 2;

  def __getitem__(self, key):
    return (self.x, self.y)[key];


  def rsq( self ):
    'Return the squared length of the vector.'
    x, y = self.x, self.y
    return ( x*x + y*y )

  def r( self ):
    'Return the length of the vector.'
    x, y = self.x, self.y
    return sqrt( x*x + y*y )

  length = r # alias

  def dot( self, other ):
    'Return the dot product of two vectors.'
    return self.x*other.x + self.y*other.y

  def radians( self ):
    'Return the angle of the vector to the x-axis in counterclockwise radians.'
    return atan2( self.y, self.x )
  def degrees( self ):
    'Return the angle of the vector to the x-axis in counterclockwise degrees.'
    return atan2( self.y, self.x )

  def rotate_90( self ):
    '''Return this vector rotated by 90 degrees counterclockwise. (In complex
    notation, equivalent to multiplying by i.)'''
    return v2( -self.y, self.x )

  def rotate( self, angle ):
    'Return this vector rotated by `angle` radians counterclockwise.'
    x, y = self.x, self.y
    c, s = cos(angle), sin(angle)
    return v2( x*c - y*s, x*s + y*c )

  def normalize( self ):
    'Return this vector normalized to a unit vector.'
    return self / self.r()


  def __add__( self, other ):
    return v2( self.x + other.x, self.y + other.y )
  def __sub__( self, other ):
    return v2( self.x - other.x, self.y - other.y )
  def __iadd__( self, other ):
    self.x += other.x
    self.y += other.y
    return self
  def __isub__( self, other ):
    self.x -= other.x
    self.y -= other.y
    return self

  def __mul__( self, other ):
    return v2( self.x * other, self.y * other )
  def __rmul__( self, other ):
    return v2( other * self.x, other * self.y )
  def __imul__( self, other ):
    self.x *= other
    self.y *= other
    return self

  def __div__( self, other ):
    return v2( self.x / other, self.y / other )
  def __truediv__( self, other ):
    return v2( self.x / other, self.y / other )
  def __idiv__( self, other ):
    self.x /= other
    self.y /= other
    return self
  def __itruediv__( self, other ):
    self.x /= other
    self.y /= other
    return self

  def __pos__( self ):
    return self
  def __neg__( self ):
    return v2( -self.x, -self.y )

  def __complex__( self ):
    return self.x + 1j*self.y


#========================================================================================
# 3D vector
#========================================================================================
class v3( object ):
  'Represents a 3D point with coordinates (x,y).'
  __slots__ = ['x','y','z']

  def __init__( self, x, y, z ):
    self.x = x
    self.y = y
    self.z = z

  '''
  @classmethod
  def polar( cls, r, radians ):
    'Construct a vector from a length and angle.'
    return cls( r*cos(radians), r*sin(radians) )

  @classmethod
  def from_angle( cls, radians ):
    'Construct a unit vector from an angle.'
    return cls( cos(radians), sin(radians) )
  '''

  def __str__( self ):
    return '(%.3f,%.3f,%.3f)' % ( self.x, self.y, self.z )
  def __repr__( self ):
    return 'v3(%r,%r,%r)' % ( self.x, self.y, self.z )

  def __eq__( self, other ):
    return self.x == other.x and self.y == other.y and self.z == other.z
  def __ne__( self, other ):
    return self.x != other.x or  self.y != other.y or self.z != other.z
  def __hash__( self ):
    return hash(( self.x, self.y, self.z ))

  def __len__(self):
    return 3;
  def __getitem__(self, key):
    return (self.x, self.y, self.z)[key];


  def rsq( self ):
    'Return the squared length of the vector.'
    x, y, z = self.x, self.y, self.z
    return ( x*x + y*y +z*z )

  def r( self ):
    'Return the length of the vector.'
    x, y, z = self.x, self.y, self.z
    return sqrt( x*x + y*y + z*z )

  length = r # alias

  def dot( self, other ):
    'Return the dot product of two vectors.'
    return self.x*other.x + self.y*other.y + self.z*other.z

  '''
  def radians( self ):
    'Return the angle of the vector to the x-axis in counterclockwise radians.'
    return atan2( self.y, self.x )
  def degrees( self ):
    'Return the angle of the vector to the x-axis in counterclockwise degrees.'
    return atan2( self.y, self.x )

  def rotate_90( self ):
    Return this vector rotated by 90 degrees counterclockwise. (In complex
    notation, equivalent to multiplying by i.)
    return v2( -self.y, self.x )
  
  def rotate( self, angle ):
    'Return this vector rotated by `angle` radians counterclockwise.'
    x, y = self.x, self.y
    c, s = cos(angle), sin(angle)
    return v2( x*c - y*s, x*s + y*c )
  '''
  def normalize( self ):
    'Return this vector normalized to a unit vector.'
    return self / self.r()

  def __add__( self, other ):
    return v3( self.x + other.x, self.y + other.y, self.z + other.z )
  def __sub__( self, other ):
    return v3( self.x - other.x, self.y - other.y, self.z - other.z )
  def __iadd__( self, other ):
    self.x += other.x
    self.y += other.y
    self.z += other.z
    return self
  def __isub__( self, other ):
    self.x -= other.x
    self.y -= other.y
    self.z -= other.z
    return self

  def __mul__( self, other ):
    return v3( self.x * other, self.y * other, self.z * other )
  def __rmul__( self, other ):
    return v3( other * self.x, other * self.y, other * self.z )
  def __imul__( self, other ):
    self.x *= other
    self.y *= other
    self.z *= other
    return self

  def __div__( self, other ):
    return v3( self.x / other, self.y / other, self.z / other )
  def __truediv__( self, other ):
    return v3( self.x / other, self.y / other, self.z / other )
  def __idiv__( self, other ):
    self.x /= other
    self.y /= other
    self.z /= other
    return self
  def __itruediv__( self, other ):
    self.x /= other
    self.y /= other
    self.z /= other
    return self

  def __pos__( self ):
    return self
  def __neg__( self ):
    return v3( -self.x, -self.y, -self.z )

  #def __complex__( self ):
  #  return self.x + 1j*self.y

#========================================================================================
# Line Segment
#========================================================================================
class line_segment( object ):
  '''Represents a directed line segment in the plane, with distinguished start
  and end points.'''
  __slots__ = [ 'start', 'end' ]

  def __init__( self, start, end ):
    self.start = start
    self.end   = end

  def __str__( self ):
    return '|%s->%s|' % ( self.start, self.end )
  def __repr__( self ):
    return 'line_segment(%r,%r)' % ( self.start, self.end )
  def render( self, surf, color, width ):
    'Render on screen.'
    pygame.draw.line(surf, color, (self.start.x, self.start.y), (self.end.x,self.end.y), width);
    pass;

  def __eq__( self, other ):
    return self.start == other.start and self.end == other.end
  def __ne__( self, other ):
    return self.start != other.start or  self.end != other.end
  def __hash__( self ):
    return hash(( self.start, self.end ))

  def __pos__( self ):
    return self
  def __neg__( self ):
    '''Reverse the line segment's direction.'''
    return line_segment( self.end, self.start )

  def v2( self ):
    return self.end - self.start;

  def length( self ):
    return self.v2().r()

  def project_t( self, pt ):
    '''Project `pt` onto the infinite line through `self` and return the
    value `t` where the projection = ``start + (end-start)*t``.
    This has the convenient property that t \in [0,1] if the projection is on
    the line segment.'''
    v = self.v2()
    rsq = float(v.rsq());                                                       ## Original version is wrong here. (no float() )
    if rsq == 0.0: return 0.0
    return (pt-self.start).dot(v) / rsq

  def project( self, pt ):
    '''Project `pt` onto the infinite line through `self` and return the
    projected point.'''
    t = self.project_t( pt )
    return self.start + self.v2()*t;

  def project_in(self, pt):
    '''Project `pt` onto the ling segment through `self` and return the
    projected point.'''
    t = self.project_t( pt )
    t = min( t, 1.0 );
    t = max( 0, t );
    return self.start + self.v2()*t;

  def intersects_segment(self, seg):
    """Determine if the line segment intersects with another line segment
    Reference: http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
    """
    def __ccw__( A, B, C ):
      """determine if three points are listed in a counterclockwise order"""
      return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x);

    A = self.start; B = self.end;
    C = seg.start;  D = seg.end;
    return __ccw__(A,C,D) != __ccw__(B,C,D) and __ccw__(A,B,C) != __ccw__(A,B,D);

  def closest_point( self, pt ):
    '''Return the closest point on the line segment to `pt`.'''
    t = self.project_t( pt )
    if   t <  0.0: return self.start
    elif t <= 1.0: return self.start + self.v2()*t
    else:          return self.end

  def dist_line_seg(self, line_seg):
    """return the closest distance between two line segments"""
    if self.intersects_segment( line_seg ):
      return 0.0;
    
    other_proj_start = self.project_in( line_seg.start );
    other_proj_end = self.project_in( line_seg.end );
    dist = [];
    dist.append( (other_proj_start - line_seg.start).r() );
    dist.append( (other_proj_end - line_seg.end).r() );
    proj_to_otehr_start = line_seg.project_in( self.start );
    proj_to_otehr_end   = line_seg.project_in( self.end );
    dist.append( (proj_to_otehr_start - self.start).r() );
    dist.append( (proj_to_otehr_end - self.end).r() );
    return min(dist);

#========================================================================================
# Circle
#========================================================================================
class circle( object ):
  'Represents a circle in the plane, with a radius and a center.'
  __slots__ = [ 'center', 'radius' ]
  def __init__( self, center, radius ):
    self.radius = radius
    self.center = center

  def __str__( self ):
    return '%.3f@%s' % ( self.radius, self.center )
  def __repr__( self ):
    return 'circle(%r,%r)' % ( self.radius, self.center )

  def __eq__( self, other ):
    return self.radius == other.radius and self.center == other.center
  def __ne__( self, other ):
    return self.radius != other.radius or  self.center != other.center
  def __hash__( self ):
    return hash(( self.radius, self.center ))


  def __and__( self, other ):
    '''``a & b``: do the circles ``a`` and ``b`` intersect? (One circle
    contained in another counts as intersecting.)'''
    return (self.center-other.center).r() < self.radius+other.radius

  def intersects_segment( self, seg ):
    'Returns whether the circle `self` and the line_segment `seg` intersect.'
    closest_pt = seg.closest_point( self.center )
    return ( closest_pt - self.center ).r() <= self.radius

  def intersect_segment( self, seg ):
    '''Returns the first intersection point between the circle `self` and the
    line_segment `seg`, or None if they do not intersect.  If `seg` starts
    inside the circle, returns the line segment's start point.'''
    v = seg.v2()

    # Project the center onto the line and find the closest point on the seg.
    t = seg.project_t( self.center )
    projected_pt = seg.start + v*t
    if   t <  0.0: return seg.start # start is inside the circle
    elif t <= 1.0: closest_pt = projected_pt
    else:          closest_pt = seg.end

    # Is the closest point inside the circle?
    r = self.radius
    if ( closest_pt - self.center ).r() > r:
      return None

    # Find the distance between the projected point and the intersection point.
    projected_distance_sq = ( projected_pt - self.center ).rsq()
    intersect_distance = sqrt( r*r - projected_distance_sq )
    return projected_pt - intersect_distance*v.normalize()


  def tangent_segments( self, other, counterclockwise ):
    '''Given two circles `self` and `other`, yield between 0 and 2 line
    segments which are tangent to both circles and whose start point lies on
    `self` going (counter)clockwise (depending on the boolean
    `counterclockwise` parameter).'''
    across  = self.tangent_segment_across ( other, counterclockwise )
    if across  is None: return ()
    between = self.tangent_segment_between( other, counterclockwise )
    if between is None: return ( across, )
    return ( across, between )

  def tangent_segment_across( self, other, counterclockwise ):
    '''Given two circles `self` and `other`, return a line_segment tangent to
    both circles which DOES NOT cross between the circles. (Or None if there is
    no such tangent line.)'''
    vc = other.center - self.center # vector from center to center
    d = vc.r()                      # distance from center to center

    ra_minus_rb = abs( self.radius - other.radius ) # difference of radii
    if d == 0.0 or d < ra_minus_rb:
      # Circles are concentric: there's no tangent line across them.
      return None

    # Compute the tangent line running across the circles.
    par  = ra_minus_rb / d
    perp = sqrt( 1.0-par*par )

    # Compute the unit vector from the circle center to the tangent point.
    if self.radius > other.radius: offset_v =   par *vc
    else:                          offset_v = (-par)*vc
    if counterclockwise:           offset_v -= perp*vc.rotate_90()
    else:                          offset_v += perp*vc.rotate_90()
    offset_v /= d

    # Compute and yield the line segment.
    return line_segment(  self.center +  self.radius*offset_v,
                         other.center + other.radius*offset_v )

  def tangent_segment_between( self, other, counterclockwise ):
    '''Given two circles `self` and `other`, return a line_segment tangent to
    both circles which DOES cross between the circles. (Or None if there is no
    such tangent line.)'''
    vc = other.center - self.center # vector from center to center
    d = vc.r()                      # distance from center to center

    ra_plus_rb = self.radius + other.radius # sum of circles' radii
    if d == 0.0 or d < ra_plus_rb:
      # Circles intersect: there's no tangent line between them.
      return None

    # Compute the tangent line running between the circles.
    par  = ra_plus_rb / d      # parallel component of offset
    perp = sqrt( 1.0-par*par ) # perpendicular component of offset

    # Compute the unit vector from the circle center to the tangent point.
    offset_v = par*vc
    if counterclockwise: offset_v -= perp*vc.rotate_90()
    else:                offset_v += perp*vc.rotate_90()
    offset_v /= d

    # Compute and yield the line segment.
    return line_segment(  self.center +  self.radius*offset_v,
                         other.center - other.radius*offset_v )

  def arc( self, from_pt, to_pt, counterclockwise ):
    '''Returns the arc extending from `from_pt` to `to_pt` on this circle, in
    the direction indicated by the `counterclockwise` parameter.'''
    start_angle = ( from_pt - self.center ).radians()
    delta_angle = (   to_pt - self.center ).radians() - start_angle
    if counterclockwise: end_angle = start_angle + delta_angle % ( 2*pi)
    else:                end_angle = start_angle + delta_angle % (-2*pi)
    return arc( self, start_angle, end_angle )

#========================================================================================
# Sphere
#========================================================================================
class sphere(object):
  'Represents a sphere in the plane'
  def __init__(self, center, radius):
    '''Constructor of a sphere.
    @param center: v2     The center of the sphere.
    @param radius: number The radius of the sphere'''
    self.center = center;
    self.radius = radius;

  def contains( self, point ):
    '''determines if a point(v2) is inside the sphere'''
    dist = (point-self.center).r();
    return dist <= self.radius;

  def intersects(self, other):
    '''determines if the sphere intersects with another sphere.
    @param other: sphere'''
    center_dist = (self.center - other.center).r();
    return center_dist <= ( self.radius + other.radius );

  def intersects_line(self, line_seg):
    circle = self.boundary_circle();
    return circle.intersects_segment(line_seg);

  def boundary_circle(self):
    return circle(self.center, self.radius);

#========================================================================================
# Path
#========================================================================================
class path( list ):
  'Represents a series of connected `line_segment` and `arc` objects.'
  def __str__( self ):
    s = 'path:'
    for element in self:
      s += '\n  ' + str(element)
    return s
  def __repr__( self ):
    s = 'path([ '
    for element in self:
      s += '%r, ' % ( element, )
    return s + ' ])'

  def length( self ):
    total = 0
    for element in self:
      total += element.length()
    return total
