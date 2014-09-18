

import sys, os, math

sys.path.append('../basics/math')
sys.path.append('../basics/robotics')

from WarehouseRobot import *
from warehouse_sampling_helper import *
from masampling  import *
from hyper_geometry import *

def main():

	WIDTH = 800;
	HEIGHT = 800;
	dimensions = [ 800 ] * 2;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	robot = WarehouseRobot(dimensions);
	#robot.render(DISPLAYSURF, None)
	#startConfig = BlockRobotConfig(100,200, 700, 600);
	#goalConfig = BlockRobotConfig(400,400, 482.5, 332.5);
	testConfig = Config([400, 400]);

	helper  = WarehouseSamplingHelper();
	sampler = MedialAxisSampler(robot, helper);
	
	'''
	random_bad_configs = sampler.random_invalid_configs( 10000, dimensions)
	for config in random_bad_configs:
		point = (int(config[0]), int(config[1]));
		pygame.draw.line( DISPLAYSURF, (0,0,0), point, point, 3 );
	'''

	random_configs = sampler.random_configs(10000, dimensions);
	ma_samples = sampler.sample_medial_axis(random_configs, dimensions, 'L2');
	sampler.save_data(ma_samples, 'WarehouseRobotMASamplesL2.txt');

	print 'Get {0} medial axis samples'.format(len(ma_samples));

	if len(ma_samples) == 0:
		return;

	for sample in ma_samples:
		point = (int(sample.center[0]), int(sample.center[1]));
		pygame.draw.circle( DISPLAYSURF, (0,250,0), point, int(sample.radius), 2 );

	#robot.set_config(testConfig);
	#robot.render(DISPLAYSURF, 200);
	
	pygame.image.save(DISPLAYSURF, 'WarehouseRobotL2.PNG');

if __name__ == '__main__':
	main();