
import sys, os, math, pygame
sys.path.append('../basics/math')
sys.path.append('../alphashape')

from hyper_geometry 	import *
from hyper_alpha_shape 	import *
from l1_geometry 		import *
from hyper_graph 		import *

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

def draw_triangles(surf, triangle_set, color = (0,200, 0)):
	for triangle in triangle_set:
		points = [ (int(triangle.spheres[0].center[2]), int(triangle.spheres[0].center[3]) ), (int(triangle.spheres[1].center[2]), int(triangle.spheres[1].center[3]) ), ( int(triangle.spheres[2].center[2]), int(triangle.spheres[2].center[3] )) ];
		pygame.draw.polygon(surf, color, points, 0);
	pygame.display.update();

def component_center(component):
	spheres = {};
	for triangle in component.dictionary.keys():
		for sphere in triangle.spheres:
			if not spheres.has_key(sphere):
				spheres[sphere] = 1;
	center = vec([0]* 4 )
	for sphere in spheres.keys():
		center += sphere.center;

	center /= len(spheres.keys());
	return center;

def draw_topology_roadmap( surf, rmp_graph_dict ):
	'''given a graph dictionary, draw the graph to a 2D canvas'''
	count = 1;	
	for node in rmp_graph_dict.keys():
		point = (0,0)
		if isinstance(node, hyper_sphere):
			point = (int(node.center[2]), int(node.center[3]));
			pygame.draw.circle(surf, (0,200,0), point, 4 );
		elif isinstance(node, Component):
			point = component_center(node);
			point = ( int(point[2]), int(point[3]) );
			draw_triangles(surf, node.dictionary, ( 0,50 * count,0 ));
			count += 1;

		neighbors = rmp_graph_dict[node];
		for neighbor in neighbors:
			if isinstance(neighbor, hyper_sphere):
				#pass;
				pygame.draw.line( surf, (0,0,0), point, (int(neighbor.center[2]), int(neighbor.center[3])) );
			elif isinstance(neighbor, Component):
				center = component_center(neighbor)
				pygame.draw.line(surf, (200,0,0), point, ( int(center[2]), int(center[3]) ), 3);

def main():

	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	sphere_set = load_data('BlockRobotMASamplesL2.txt', 'L2');

	for sphere in sphere_set:
		point = (int(sphere.center[2]), int(sphere.center[3]));
		pygame.draw.circle( DISPLAYSURF, (220,220,220), point, int(sphere.radius), 2 );
	
	alphashape = Nerve();
	edges, triangle_set, graph_dict, edge_tri_dict = alphashape.nerve(sphere_set);

	#draw_topology_roadmap(DISPLAYSURF, graph_dict)
	#draw_triangles(DISPLAYSURF, triangle_set);
	
	components = alphashape.contract(triangle_set, edge_tri_dict);
	#print len(components)
	i = 1;
	for component in components:
		draw_triangles(DISPLAYSURF, component, (0,50 * i, 50 * i));
		i += 1;


	rmp_graph_dict = alphashape.build_topology_roadmap(components,graph_dict);
	
	#print len(rmp_graph_dict.keys())

	draw_topology_roadmap(DISPLAYSURF, rmp_graph_dict)
	

	graph = Graph(rmp_graph_dict);

	start = vec([400,400, 100, 400]);
	end   = vec([400, 400, 700, 400]);

	start_node = graph.find_node(start);
	end_node   = graph.find_node(end);

	print start_node;
	print end_node

	paths = graph.find_all_paths(start_node, end_node);
	print len(paths);
	i = 0;
	for path in paths:
		i += 1
		print '================'
		for node in path:
			if isinstance(node, hyper_sphere):
				point = ( int(node.center[2]), int(node.center[3]) )
				print point
				pygame.draw.circle(DISPLAYSURF, (70*i,0,0), point, 10 );
			elif isinstance(node, Component):
				center = component_center(node);
				point = ( int(center[2]), int(center[3]) );
				print point
				pygame.draw.circle(DISPLAYSURF, (70*i,0,0), point, 10 );


	pygame.image.save(DISPLAYSURF, 'roadmap.PNG');

	pass;


if __name__ == '__main__':
	main();