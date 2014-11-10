The basic idea of Devin's representation is that:
If we regard the robot in workspace as a set of infinite particles, 
the state of robot can be represented using the positions of all particles.
Thus, we will have a Euclidean space with infinite number of dimensions as C-space.

However, in order to plan motions, we need to have a parameterized C-space so that 
any state can be uniquely represented by finite parameters.

So we have three spaces:
1. Workspace
	A 3D( or 2D ) Euclidean space. Collision detection and  are done here. We can also
	get collision distance(time) here.
2. Configuration Space:
	By regarding a robot as infinite number of particles, we can build a C-space with
	infinite number of dimensions. 
3. Parameterized Configuration Space.
	Motion planning happens here. 