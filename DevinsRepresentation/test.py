

import sys, os, math, pygame

sys.path.append('../basics/math')

from geometry import *
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
	origin_param_state = robot.get_param_state();

	robot.render(DISPLAYSURF, (255,0,0));
	disp_dist = 200;
	
	'''
	# These code get random states with disp_dist distance to original one. 
	# =================================================
	states = [];
	for i in range(10000):
		rnd_state = robot.get_random_state(disp_dist);
		if math.fabs(robot.displacement_dist(rnd_state) - disp_dist) <= 0.01:
			states.append( rnd_state );

	print len(states)

	param_states = [];
	for i in range(len(states)):
		robot.set_state(states[i]);
		param_state = robot.get_param_state()
		color = (v2(param_state[0], param_state[1]) - v2(origin_param_state[0], origin_param_state[1])).r();
		param_states.append( (param_state[0],param_state[1],param_state[2],color ) );
		#param_states.append( (param_state[0],param_state[1],param_state[2]+math.pi*2,color ) );
		#robot.render(DISPLAYSURF, (0, 50 + i * 200/len(states) ,0), 1);
		robot.render_head(DISPLAYSURF)

	#pygame.image.save(DISPLAYSURF, "displacement_dist.PNG");
	pygame.image.save(DISPLAYSURF, "head_pos.PNG");
	save(states, 'cspace.txt');
	save(param_states, 'param_cspace.txt');
	'''

	
	# These code classify previous states into 4 groups
	# based on vertices of the rigid body.
	# =================================================
	p1group, p2group, p3group, p4group = robot.get_classified_random_states(1000, disp_dist);
	DISPLAYSURF1 = DISPLAYSURF.copy();
	DISPLAYSURF2 = DISPLAYSURF.copy();
	DISPLAYSURF3 = DISPLAYSURF.copy();
	DISPLAYSURF4 = DISPLAYSURF.copy();
	for state in p1group:
		robot.set_state(state);
		robot.render(DISPLAYSURF,  (250,0,0), 1 );
		robot.render(DISPLAYSURF1, (250,0,0), 1 );
	for state in p2group:
		robot.set_state(state);
		robot.render(DISPLAYSURF,  (0,250,0), 1 );
		robot.render(DISPLAYSURF2, (0,250,0), 1 );
	for state in p3group:
		robot.set_state(state);
		robot.render(DISPLAYSURF,  (0,0,250), 1 );
		robot.render(DISPLAYSURF3, (0,0,250), 1 );
	for state in p4group:
		robot.set_state(state);
		robot.render(DISPLAYSURF,  (150,150,150), 1 );
		robot.render(DISPLAYSURF4, (150,150,150), 1 );
	
	pygame.image.save(DISPLAYSURF, "classified_displacement_dist.PNG");
	pygame.image.save(DISPLAYSURF1, "classified_p1_group.PNG");
	pygame.image.save(DISPLAYSURF2, "classified_p2_group.PNG");
	pygame.image.save(DISPLAYSURF3, "classified_p3_group.PNG");
	pygame.image.save(DISPLAYSURF4, "classified_p4_group.PNG");
	save(p1group, 'classified_p1_group.txt');
	save(p2group, 'classified_p2_group.txt');
	save(p3group, 'classified_p3_group.txt');
	save(p4group, 'classified_p4_group.txt');
	

if __name__ == '__main__':
	main()