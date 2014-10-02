
import sys, os, random, math, pygame

width  = 600;
height = 600;

def save_data( samples, filename ):
	'''Save sampled spheres. Write data to a file'''
	file2write = open( filename, 'w' );
	formattedData = "";
	for sphere in samples:
		for i in range(0, 2):
			formattedData += str( sphere[i] ) + "\t";
		formattedData += str( sphere[2]);
		formattedData += "\n";

	file2write.write( formattedData );
	file2write.close();

def inside(sphere, point):
	'''@param sphere: (x,y,r)
	@param point: (x,y)'''
	if (sphere[0]-point[0])**2 + (sphere[1]-point[1])**2 < (sphere[2]*1)**2:
		return True;
	if point[0] <= 400 and point[0] >= 300 and point[1] <= 400 and point[1] >= 300:
		return True;

def sample_one(n, samples):
	global width;
	global height;
	failed_times = 0;
	while failed_times < n:
		rand_x = random.randint(200, width-150);
		rand_y = random.randint(250, height-150);
		point = ( rand_x, rand_y );
		r = 40;
		good_sample = True;
		for sample in samples:
			if inside(sample, point):
				failed_times += 1;
				good_sample = False;
				break;
		if good_sample:
			return ( rand_x, rand_y, r );
	return None;

def sample(n):
	samples = [];
	while True:
		sample = sample_one(n, samples);
		if sample is None:
			return samples;
		samples.append(sample);

def main():
	WIDTH  = 650;
	HEIGHT = 650;

	pygame.init();
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT));
	DISPLAYSURF.fill((255,255,255));
	pygame.display.update();

	spheres = sample(10000);

	for sphere in spheres:
		center = (int(sphere[0]), int(sphere[1]));
		radius = int(sphere[2]);

		pygame.draw.circle( DISPLAYSURF, (250,0,0), center, radius );
	for sphere in spheres:
		center = (int(sphere[0]), int(sphere[1]));
		radius = int(sphere[2]);

		pygame.draw.circle( DISPLAYSURF, (0,0,0), center, radius, 1 );
	pygame.display.update();

	pygame.image.save( DISPLAYSURF, 'experiment.PNG' );
	save_data(spheres, 'experiment.txt')

if __name__ == '__main__':
	main()
