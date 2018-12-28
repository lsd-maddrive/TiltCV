import numpy as np

alpha = 0.4
beta = 1 - alpha

new_coordinates = 0
old_coordinates = None

# while loop
# reading
x = 3
y = 5
r = 3

new_coordinates = np.array([x, y, r])

if old_coordinates is None:
	old_coordinates = new_coordinates

valid_coordinates = new_coordinates * alpha + old_coordinates * beta	

old_coordinates = new_coordinates


print(valid_coordinates)


# while(1):
# 	new_coordinates = np.array([x, y, r])

# 	valid_coordinates = new_coordinates * alpha + old_coordinates * beta
	
# 	old_coordinates = new_coordinates

