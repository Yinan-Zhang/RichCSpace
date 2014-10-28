import sys, os, math, random, pygame, pdb

sys.path.append('..')
sys.path.append('../../basics/math')
sys.path.append('../../alphashape')

from geometry 		import *
from hyper_geometry import *
from Triangle   	import *

from mpl_toolkits.mplot3d import Axes3D
import pylab as pl
from matplotlib import cm
import numpy as np

fig = pl.figure();
ax = pl.axes( projection = '3d' );

def plot_points( spheres):
	print "Plotting {0} spheres".format( len(spheres) );
	pl.cla();
	ax = pl.axes( projection = '3d' );
	x = []; y = []; z = []; r = [];
	for s in spheres:
		x.append(s.center[0]);
		y.append(s.center[1]);
		z.append(s.center[2]);
		r.append(s.radius**2 * math.pi);
	x = np.array(x);
	y = np.array(y);
	z = np.array(z);
	r = np.array(r);
	c = x + y;	
	ax.scatter( x, y, z, c=c, s = r, alpha=0.7 );
	ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
	pl.show();

def generate_random_samples( n, dim ):
	'''generate n random spheres in dim dimensional space.'''
	
	spheres = [];
	while len(spheres) != n:
		coord = [0] * dim;
		for i in range(dim):
			coord[i] = random.randint(0, 100);
		center = vec(coord)
		good = True;
		for s in spheres:
			if s.contains( center ):
				good = False;
				break;
		if good:
			sphere = hyper_sphere(center, 50);
			spheres.append(sphere);
		pass

	return spheres;

def detail_sample_once( init_spheres ):
	#pdb.set_trace();
	triangulator = Triangulator(init_spheres);
	triangle_set = triangulator.triangulate_raw();

	triangle_list = triangle_set.keys();
	# clear screen
	# draw triangles
	plot_points(init_spheres);

	spheres = init_spheres;
	for tri in triangle_set.keys():
		if tri.is_semi_filled():
			radical_center = tri.radical_center();
			#print radical_center;
			new_sample = hyper_sphere(radical_center, 50);
			spheres.append(new_sample);

	return spheres;

def detail_sample( init_spheres, rounds ):
	spheres = init_spheres;
	for i in range( rounds ):
		# clear screen
		# draw spheres
		spheres = detail_sample_once(spheres);

	# draw spheres 
	plot_points(spheres);
	return spheres;

def main():
	init_spheres = generate_random_samples(20, 3);
	detail_sample(init_spheres, 3);
	pl.close()
	pass;

if __name__ == '__main__':
	main();



