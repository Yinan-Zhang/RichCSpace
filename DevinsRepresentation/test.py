

import sys, os, math, pygame
from rigid2d import *

def save(iterable, filename):
	file2write = open(filename, 'w');
	string2write = ''
	for tple in iterable: # Assume every element is a tuple
		for elem in tple:
			string2write += str(elem) + '\t'
		string2write += '\n'

	file2write.write(string2write);
	file2write.close();

def main():
	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	state = ( 400, 400, 400, 400+40 );
	robot = Rigid2D(state);

	robot.render(DISPLAYSURF, (255,0,0));
	disp_dist = 100;
	states = [];
	for i in range(100):
		states.append( robot.get_random_state(disp_dist) );

	param_states = [];
	for i in range(len(states)):
		robot.set_state(states[i]);
		param_states.append(robot.get_param_state());
		robot.render(DISPLAYSURF, (0, 50 + i * 200/len(states) ,0));

	pygame.image.save(DISPLAYSURF, "displacement_dist.PNG");
	save(states, 'cspace.txt');
	save(param_states, 'param_cspace.txt');


if __name__ == '__main__':
	main()