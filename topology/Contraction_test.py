import sys, os, math, pygame
sys.path.append('../basics/math')
sys.path.append('../alphashape')

from time				import sleep
from hyper_geometry		import *
from Contraction		import *
from l1_geometry		import *
from hyper_graph		import *
from Triangle 			import *

def load_data(filename, mode):
	'''load spheres information from file'''
	file2read = open( filename, 'r' );
	spheres = [];
	for line in file2read:
		strSphere = line;
		info = strSphere.split( '\t' );
		center = [0] * (len(info)-1);
		for i in range(0, len(info)-1):
			center[i] = float(info[i]);
		radius = float(info[len(info)-1]);
		#sphere = l1_sphere(center, radius);
		if mode == 'L2' or mode=='l2':
			sphere = hyper_sphere(center, radius)
		elif mode == 'L1' or mode == 'l1':
			sphere = l1_sphere(center, radius)
		spheres.append(sphere);
	return spheres;


def draw_triangles(surf, triangle_set, color = (200,200, 200)):
	for triangle in triangle_set:
		points = [ (int(triangle.spheres[0].center[0]), int(triangle.spheres[0].center[1]) ), (int(triangle.spheres[1].center[0]), int(triangle.spheres[1].center[1]) ), ( int(triangle.spheres[2].center[0]), int(triangle.spheres[2].center[1] )) ];
		pygame.draw.polygon(surf, color, points, 1);
	pygame.display.update();


def main():

	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	print 'Start Loading'
	sphere_list = load_data('../sampling/experiments/experiment.txt', 'L2');
	print 'Start Rendering Spheres'
	for sphere in sphere_list:
		pygame.draw.circle( DISPLAYSURF, (200, 200, 200), (int(sphere.center[0]), int(sphere.center[1])), int(sphere.radius), 1 );
	
	triangulator = Triangulator(sphere_list);

	triangle_set, sphere_tri_dict, edge_tri_dict = triangulator.triangulate();

	draw_triangles(DISPLAYSURF, triangle_set);

	contractor = Contraction(sphere_list, DISPLAYSURF);

	components = contractor.contract(triangle_set, edge_tri_dict, sphere_tri_dict);

	print "Got {0} component(s)".format(len(components))

	i = 1;
	for comp in components:
		color = (160/len(components) * i, 200/len(components) * i, 100/len(components) * i );
		comp.render(DISPLAYSURF, color);
		#print comp.get_spheres();
		i+=1

	pygame.display.update();

	pygame.image.save(DISPLAYSURF, "components.PNG")



if __name__ == '__main__':
	main();
