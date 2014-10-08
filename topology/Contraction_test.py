import sys, os, math, pygame
sys.path.append('../basics/math')
sys.path.append('../alphashape')

from time				import sleep
from hyper_geometry		import *
from Contraction		import *
from l1_geometry		import *
from hyper_graph		import *
from Triangle 			import *
from geometry 			import *
from Homotopy 			import *

def contains(s, pnt):
	return (s.center[0]-pnt[0])**2 + (s.center[1]-pnt[1])**2 < s.radius**2;

def get_path_nodes(path, spheres):
	i = 0;
	sphlist = {};
	for i in range(len(path)-1):
		dir = v2(path[i+1][0]-path[i][0], path[i+1][1]-path[i][1]) / 50.0;
		for j in range(1, 51):
			pnt = v2(path[i][0], path[i][1]) + j*dir;
			for s in spheres:
				if contains(s, pnt):
					sphlist[s] = 1;
					
	return sphlist.keys();

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

def draw_circles(surf, color, spheres):
	for sphere in spheres:
		pygame.draw.circle( surf, color, (int(sphere.center[0]), int(sphere.center[1])), int(sphere.radius), 4 );
	pygame.display.update()

def draw_path(surf, color, path ):
	for i in range(len(path)-1):
		pygame.draw.line(surf, color, path[i], path[i+1], 5);
	pygame.display.update()

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
	spheres = {}
	for sphere in sphere_list:
		spheres[sphere] = 1;
		#pygame.draw.circle( DISPLAYSURF, (200, 200, 200), (int(sphere.center[0]), int(sphere.center[1])), int(sphere.radius), 1 );

	pygame.display.update();

	##################################################
	######        Triangulate sphere centers
	triangulator = Triangulator(sphere_list);

	triangle_set, sphere_tri_dict, edge_tri_dict = triangulator.triangulate();

	#draw_triangles(DISPLAYSURF, triangle_set);


	##################################################
	######        Contruct components
	contractor = Contraction(sphere_list, DISPLAYSURF);
	#components = contractor.contract(triangle_set, edge_tri_dict, sphere_tri_dict);

	#print "Got {0} component(s)".format(len(components))
	'''
	i = 1;
	for comp in components:
		color = (160/len(components) * i, 200/len(components) * i, 100/len(components) * i );
		comp.render(DISPLAYSURF, color);
		#print comp.get_spheres();
		i+=1

	pygame.display.update();
	#time.sleep(5);
	'''

	##################################################
	######        Contruct Path
	path1 = [ (214, 261), (458, 257) ]
	path2 = [ (214, 261), (345, 290), (458, 257) ]
	path3 = [ (214, 261), (271, 431), (404, 404), (458, 257) ]

	untouchable1 = get_path_nodes(path1, sphere_list)
	untouchable2 = get_path_nodes(path2, sphere_list)
	untouchable3 = get_path_nodes(path3, sphere_list)

	draw_path(DISPLAYSURF, (0,0,250), path1);
	draw_path(DISPLAYSURF, (0,0,250), path2);
	#draw_path(DISPLAYSURF, (0,0,250), path3);
	#draw_circles(DISPLAYSURF, (250, 150, 150), untouchable1);
	#draw_circles(DISPLAYSURF, (150, 250, 150), untouchable2);
	#draw_circles(DISPLAYSURF, (150, 150, 250), untouchable3);
	pygame.display.update();
	time.sleep(1);
	#pygame.image.save(DISPLAYSURF, "homotopy.PNG")
	#return;
	
 
	##################################################
	######        determine path homotopy
	'''
	new_comp = components[0].merge(components[1],edge_tri_dict, sphere_tri_dict)

	untouchable = {}
	for s in untouchable1:
		untouchable[s] = 1;
	for s in untouchable2:
		untouchable[s] = 1;

	betti = new_comp.remove_spheres(untouchable, edge_tri_dict, sphere_tri_dict, DISPLAYSURF);
	if betti == 0:
		print "!!!!!!!! Same Homotopy"
	else:
		print "~~~~~~~~ Different Homotopy"

	pygame.image.save(DISPLAYSURF, "homotopy.PNG")
	'''

	print untouchable1;
	print untouchable2;

	union1 = SphereUnion(untouchable1[0]);	untouchable1.remove(untouchable1[0]);
	union2 = SphereUnion(untouchable2[0]);	untouchable2.remove(untouchable2[0]);
	while len(untouchable1) != 0:
		for sphere in untouchable1:
			if union1.add_sphere_betti(sphere, 0, edge_tri_dict, sphere_tri_dict):
				untouchable1.remove(sphere)

	while len(untouchable2) != 0:
		for sphere in untouchable2:
			if union2.add_sphere_betti(sphere, 0, edge_tri_dict, sphere_tri_dict):
				untouchable2.remove(sphere)


	print len(union1.get_spheres()), len(untouchable1)

	csp = HomotopyCSP(spheres, contractor.graph, triangle_set, edge_tri_dict, sphere_tri_dict);
	csp.greedy( union1, union2, DISPLAYSURF );
	pygame.image.save(DISPLAYSURF, "homotopy.PNG")

if __name__ == '__main__':
	main();
