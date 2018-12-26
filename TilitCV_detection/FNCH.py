

	alpha = 0.4
	beta = 1 - alpha

	new_coordinates = 0
	old_coordinates = 0


while(1):
	new_coordinates = np.array([x, y, r])

	valid_coordinates = new_coordinates * alpha + old_coordinates * beta
	
	old_coordinates = new_coordinates

