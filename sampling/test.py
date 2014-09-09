

import sys, os, math

sys.path.append('../basics/math')
sys.path.append('../basics/robotics')

from BlockRobots import *
from masampling  import *

def main():
	WIDTH = 800;
	HEIGHT = 800;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	robot = BlockRobot();
	startConfig = BlockRobotConfig(100,200, 700, 600);
	goalConfig = BlockRobotConfig(400,400, 482.5, 332.5);
	testConfig = BlockRobotConfig(400, 400, 460, 500);

	helper  = BlockSamplingHelper();
	sampler = MedialAxisSampler(robot, helper);

	dimensions = [ 800 ] * 4;
	random_configs = sampler.random_configs(4, 1000, dimensions);
	ma_samples = sampler.sample_medial_axis(random_configs, dimensions);
	sampler.save_data(ma_samples, 'BlockRobotMASamples.txt');

	print 'Get {0} medial axis samples'.format(len(ma_samples));

	for i in range( 0, len(ma_samples)):
		robot.set_config( ma_samples[i].center );
		robot.render(DISPLAYSURF, (i+1) * 255/len(ma_samples));

	#robot.set_config( goalConfig );
	#robot.render(DISPLAYSURF, 250);
	#pygame.display.update();

	pygame.image.save(DISPLAYSURF, 'BlockRobot.PNG');

if __name__ == '__main__':
	main();