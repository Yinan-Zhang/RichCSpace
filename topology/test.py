
import sys, os, math, pygame
sys.path.append('../basics/math')
sys.path.append('../alphashape')

from hyper_geometry 	import *
from hyper_alpha_shape 	import *
from l1_geometry 		import *
from hyper_graph 		import *

def load_data(filename):
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
		sphere = l1_sphere(center, radius);
		spheres.append(sphere);
	return spheres;

def draw_triangles(surf, triangle_set):
	for triangle in triangle_set:
		points = [ (int(triangle.spheres[0].center[2]), int(triangle.spheres[0].center[3]) ), (int(triangle.spheres[1].center[2]), int(triangle.spheres[1].center[3]) ), ( int(triangle.spheres[2].center[2]), int(triangle.spheres[2].center[3] )) ];
		pygame.draw.polygon(surface, (0,200, 0), points);

def draw_topology_roadmap( surf, graph_dict ):
	'''given a graph dictionary, draw the graph to a 2D canvas'''	
	
	

def main():
	spheres = load_data('BlockRobotMASamplesL1.txt');
	alphashape = Nerve();
	edges, triangle_set, graph_dict, edge_tri_dict = alphashape.nerve(spheres);
	new_graph_dict = alphashape.build_topology_roadmap(sphere_set, triangle_set, edge_tri_dict, graph_dict);
	graph = hyper_graph(new_graph_dict);

	pass;


if __name__ == '__main__':
	main();