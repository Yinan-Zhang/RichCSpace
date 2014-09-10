

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
	#startConfig = BlockRobotConfig(100,200, 700, 600);
	#goalConfig = BlockRobotConfig(400,400, 482.5, 332.5);
	testConfig = BlockRobotConfig(400, 400, 350, 400);

	helper  = BlockSamplingHelper();
	sampler = MedialAxisSampler(robot, helper);

	dimensions = [ 800 ] * 4;
	
	random_bad_configs = sampler.random_invalid_configs( 4, 5000, dimensions)
	for config in random_bad_configs:
		point = (int(config[2]), int(config[3]));
		pygame.draw.line( DISPLAYSURF, (0,0,0), point, point, 3 );

	random_configs = sampler.random_configs(4, 2000, dimensions);
	ma_samples = sampler.sample_medial_axis(random_configs, dimensions, 'L1');
	sampler.save_data(ma_samples, 'BlockRobotMASamples.txt');

	print 'Get {0} medial axis samples'.format(len(ma_samples));

	if len(ma_samples) == 0:
		return;

	for sample in ma_samples:
		point = (int(sample.center[2]), int(sample.center[3]));
		pygame.draw.circle( DISPLAYSURF, (0,250,0), point, int(sample.radius), 2 );

	#robot.set_config(testConfig);
	#robot.render(DISPLAYSURF, 200);

	pygame.image.save(DISPLAYSURF, 'BlockRobot.PNG');

if __name__ == '__main__':
	main();